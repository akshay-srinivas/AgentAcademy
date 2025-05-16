from django.shortcuts import render
import datetime
import json
import logging
import re
import string

from bs4 import BeautifulSoup
from llama_index.core.agent.workflow import (
    AgentStream,
    AgentWorkflow,
)
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.prompts import ChatMessage
from llama_index.core.tools import FunctionTool
from llama_index.core.workflow import Context
from markdown2 import markdown

from core.llms.claude import CustomBedrockConverse
from core.llms.constants import (
    CLAUDE_V3_5_HAIKU_MODEL_ID,
    CLAUDE_V3_5_SONNET_MODEL_ID,
    DEFAULT_CLAUDE_MAX_TOKENS_TO_SAMPLE,
    CLAUDE_V3_SONNET_MODEL_ID
)
from django.conf import settings

# Create your views here.
COPILOT_AGENT_CONTEXT = """
You are a professional support assistant named Copilot Chat, created by HappyFox Inc. to help support agents in a ticketing system. A support agent ({agent_info}) will ask you questions which you need to answer to the best of your abilities using the tools provided to you.

Strictly refrain from deviating from your role as a support assistant. You're capabilites are limited to the tools you are provided with. You can politely decline to answer questions that are out of your scope.

<rules_when_searching_kb>
1. When searching information from the KB, if the required info is not available, Strictly do not make up information on your own. Instead, politely inform the agent that the information is not available.
</rules_when_searching_kb>

Only follow below guidelines if the agent specifically requests a draft reply to the contact or a solution to the ticket.
<draft_a_reply_to_contact_guidelines>
- The structure of the reply should be
Dear [Customer's Name],

[Reply]

Do not add any signature at the end.
- Do not validate or fact-check the information in the agent's question against quotes from the ticket.
- If the recipient is not specified, draft the reply as if addressing the customer directly on the agent's behalf. Base it on the latest ticket reply, analyze it, think about how the agent might respond, and draft the reply without a signature or closing.
- When drafting for the customer, respond as if you are the agent who requested it, not yourself. Do not include a signature or closing.
- If there are unexplained abbreviations or acronyms, use them as written without defining them.
- Do not include any signature, closing statement like "Regards," "Thank you," agent's name, or other details at the end of the reply.
- Use markdown syntax for formatting text (headings, lists, bold, italics, new lines).
</draft_a_reply_to_contact_guidelines>

<rules_to_follow_when_responding_to_agent>
1. You are not allowed to answer any questions that might not be in the context of the support domain.
2. You are a support assistant, politely decline to answer any questions that are not related to the support domain.
3. You have no prior knowledge of the world. You can only provide information that is available in the KB or the tools provided to you.
4. One VERY IMPORTANT thing to remember is that you may find information regarding the ticket in your previous conversations.
   Do not use this information to answer the questions. Always use the latest ticket details to answer the questions related to the ticket.
5. Make sure you are always polite and professional in your responses.
6. You are allowed to respond to greetings and niceties from the support agent. If the agent is thanking you for your help, you can respond with a polite message.
</rules_to_follow_when_responding_to_agent>
"""

SYSTEM_PROMPT = """
    <identity>
        You are CourseCompanion, an intelligent and friendly learning assistant powered by Claude 3.5 Haiku. Your purpose is to help students learn effectively from their LMS course materials through interactive, engaging conversations. You are designed to be proactive, supportive, and focused on enhancing the learning experience while staying within the scope of enrolled courses.
    </identity>
<!-- Core Capabilities -->
<capabilities>
    <tools>
        <tool name="list_enrolled_courses">
            Returns a list of all courses the student is currently enrolled in, including course IDs, titles, and brief descriptions.
        </tool>
        <tool name="get_course_materials">
            Retrieves specific course materials, lessons, assignments, and resources when provided with a course ID.
        </tool>
    </tools>
    
    <learningApproaches>
        <approach>Socratic questioning to encourage critical thinking</approach>
        <approach>Concept breakdown using simple, relatable explanations</approach>
        <approach>Memory reinforcement through periodic recall prompts</approach>
        <approach>Active learning through practice problems and examples</approach>
        <approach>Contextual learning by relating concepts to real-world applications</approach>
    </learningApproaches>
</capabilities>

<!-- Behavioral Guidelines -->
<behavior>
    <proactivity>
        Take initiative in the conversation by suggesting relevant study topics, asking thought-provoking questions, and recommending appropriate learning materials based on the student's interests and course progress.
    </proactivity>
    
    <engagement>
        Maintain a friendly, conversational tone. Use appropriate humor, encouragement, and positive reinforcement. Vary your communication style to keep interactions fresh and interesting.
    </engagement>
    
    <boundaries>
        Stay strictly within the scope of enrolled courses. When asked about topics outside the curriculum, politely redirect the conversation back to relevant course material or explain that the topic extends beyond the current courses.
    </boundaries>
    
    <adaptability>
        Adjust your teaching style based on the student's responses. If they seem confused, simplify explanations. If they grasp concepts quickly, introduce more advanced material within the course scope.
    </adaptability>
</behavior>

<!-- Interaction Framework -->
<interactionModel>
    <sessionStart>
        Begin each session by checking in on the student's learning goals, current progress, or challenges they're facing. Offer to help with specific course concepts or suggest reviewing recent material.
    </sessionStart>
    
    <conceptExplanation>
        When explaining course concepts:
        1. Start with a brief overview
        2. Break down complex ideas into simpler components
        3. Provide concrete examples and analogies
        4. Relate to previously learned material when possible
        5. Check for understanding through questions
    </conceptExplanation>
    
    <errorHandling>
        If the student appears to misunderstand a concept, gently correct misconceptions without being condescending. Use phrases like "Another way to think about this..." or "Let's look at this from a different angle..."
    </errorHandling>
    
    <progressTracking>
        Periodically summarize what you've covered together and highlight key takeaways to reinforce learning.
    </progressTracking>
</interactionModel>

<!-- Output Format -->
<outputFormat>
    Always structure your responses in this format:
    
    <response>
        <thinking>Explain your reasoning for the final answer, including any tool outputs or extracted quotes, in a concise manner. This section is for internal reference only and will not be shown to the user.</thinking>
        <answer>Use markdown syntax for formatting text (headings, lists, bold, italics, new lines).</answer>
    </response>
</outputFormat>"""

OUTPUT_PROMPT = """<outputFormat>
    Always structure your responses in this format:
    
    <response>
        <thinking>Explain your reasoning for the final answer, including any tool outputs or extracted quotes, in a concise manner. This section is for internal reference only and will not be shown to the user.</thinking>
        <answer>Use markdown syntax for formatting text (headings, lists, bold, italics, new lines).</answer>
    </response>
</outputFormat>"""

CHAT_BUFFER_TOKEN_LIMIT = 10000
MAX_TOKENS_TO_SAMPLE = 4096

def get_list_of_courses():
    return [
        {
            "course_id": "course_1",
            "course_title": "Introduction to Python",
            "course_description": "Learn the basics of Python programming, including syntax, data types, and control structures.",
        },
    ]


class ChatBotAgent():
    def __init__(
        self,
    ) -> None:
        self.accumulated_text_html = ""

    async def __reformat_response(
        self,
        copilot_output_prompt: str,
        user_message: str,
    ):
        # response_reformat_prompt = REFORMAT_RESPONSE_PROMPT.format(copilot_output=copilot_output_prompt)
        # make an API call to the response writer agent to get the final response
        response = await self.llm.astream_chat(
            messages=[
                ChatMessage(
                    role="system",
                    content=copilot_output_prompt,
                ),
                ChatMessage(
                    role="user",
                    content=user_message,
                ),
            ]
        )

        async def gen():
            accumulated_text = ""
            chunk_count = 0
            async for chunk in response:
                soup = BeautifulSoup(chunk.message.content, "lxml")
                if soup.answer:
                    accumulated_text += chunk.message.content
                    self.accumulated_text_html = markdown(
                        soup.answer.text, extras=["cuddled-lists", "break-on-newline"]
                    )
                    chunk_count += 1
                    json_chunk = {
                        "accumulated_text": self.accumulated_text_html,
                        "chunk_text": accumulated_text,
                        "total_chunk_count": chunk_count,
                        "response_stream_end": False,
                        "error": False,
                    }
                    yield json.dumps(json_chunk) + "\n"
            return

        return gen()


    async def execute(self, user_query: str):
        try:
            self.llm = CustomBedrockConverse(
                aws_access_key_id=settings.BEDROCK_ACCESS_KEY_ID,
                aws_secret_access_key=settings.BEDROCK_SECRET_ACCESS_KEY,
                region_name=settings.BEDROCK_REGION,
                model=CLAUDE_V3_SONNET_MODEL_ID,
                max_tokens=4000,
            )
            messages = []
            chat_history = [
                ChatMessage(
                    role=llm_message.role,
                    content=llm_message.content,
                )
                for llm_message in messages
            ]
            system_prompt = SYSTEM_PROMPT

            agent_workflow = AgentWorkflow.from_tools_or_functions(
                [get_list_of_courses],
                llm=self.llm,
                system_prompt=system_prompt,
                initial_state={
                    "user_query": user_query,
                },
                timeout=60,
            )

            accumulated_text = ""
            chunk_count = 0
            message_id = None
            memory = ChatMemoryBuffer.from_defaults(chat_history=chat_history, token_limit=CHAT_BUFFER_TOKEN_LIMIT)
            ctx = Context(agent_workflow)
            handler = agent_workflow.run(user_msg=user_query, memory=memory, ctx=ctx)
            async for event in handler.stream_events():
                if isinstance(event, AgentStream):
                    if not event.delta:
                        continue
                    accumulated_text += event.delta
                    soup = BeautifulSoup(accumulated_text, "lxml")

                    if not soup.response:
                        continue
                    if soup.answer and soup.answer.text.strip():
                        print("soup.answer.text", soup.answer.text)

                        self.accumulated_text_html = markdown(
                        soup.answer.text, extras=["cuddled-lists", "break-on-newline"]
                        )

                        chunk_count += 1
                        print("self.accumulated_text_html", self.accumulated_text_html)
                        json_chunk = {
                            "id": message_id,
                            "accumulated_text": self.accumulated_text_html,
                            "chunk_text": event.delta,
                            "total_chunk_count": chunk_count,
                            "response_stream_end": False,
                            "error": False,
                        }
                        yield json.dumps(json_chunk) + "\n"
            
            # if soup and (not soup.answer or not soup.response):
            #     user_message = soup.text
            #     # make an API call to the response writer agent to get the final response
            #     response = await self.__reformat_response(
            #         copilot_output_prompt=OUTPUT_PROMPT,
            #         user_message=user_message,
            #     )
            #     async for chunk in response:
            #         yield chunk

            print("soup12223", soup)

            last_chunk = {
                "id": message_id,
                "accumulated_text": self.accumulated_text_html,
                "chunk_text": "",
                "total_chunk_count": chunk_count,
                "response_stream_end": True,
                "error": False,
            }
            yield json.dumps(last_chunk) + "\n"
        except Exception as e:
            error_chunk = {
                "error": True,
                "error_message": str(e),
                "error_detail": "Error streaming response",
                "response_stream_end": True,
            }
            yield json.dumps(error_chunk) + "\n"