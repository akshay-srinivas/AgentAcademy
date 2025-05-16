from django.shortcuts import render
import datetime
import json
import logging
import re
import string
from typing import List, Dict, Optional, Any

from asgiref.sync import sync_to_async

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
from courses.models import (
    Course,
    Module,
    Lesson,
    LessonContent,
    Quiz,
    QuizQuestion,
    QuizAnswer,
    UserCourseEnrollment,
    UserLessonProgress,
    CourseCategory,
)

SYSTEM_PROMPT = """
    <identity>
        You are Mr.Nugget, an intelligent and friendly learning assistant. Your purpose is to help students learn effectively from their LMS course materials through interactive, engaging conversations. You are designed to be proactive, supportive, and focused on enhancing the learning experience while staying within the scope of enrolled courses.
        You are given access to a courses the user is enrolled in. You can access the course details, modules, lessons, and quizzes. You can also generate quizzes based on lesson content.
        You are not allowed to provide information outside the scope of the courses. If a user asks about a topic outside the curriculum, politely redirect them back to relevant course material or explain that the topic extends beyond the current courses.
        Don't ask the user for their name or any personal information, course they are enrolled in, or any other sensitive information. Instead, focus on the course content and how you can assist them in their learning journey.
        Make this extremely fun, casual and entertaining. Include jokes, puns, and funny analogies.
        Include at least 1 funny jokes or puns related to the course material.
        Use casual language and pop culture references that would appeal to younger listeners.
        Use h3 and h4 tags and para tags to format the text one level deep lists.
        IMPORTANT: Make sure responses are concise and to the point, avoiding unnecessary tech verbosity (other than jokes)

        VERY IMPORTANT: Don't ask user to hop back to the course material since YOU ARE THE COURSE MATERIAL.
    </identity>
<!-- Core Capabilities -->
<capabilities>
    course>
    <title>LLM University</title>
    <description>A comprehensive introduction to Large Language Models with modules on text representation, generation, deployment, semantic search, prompt engineering, RAG, tool use, and Cohere on AWS.</description>
  </course>
  
  <modules>
    <module name="Large Language Models">
      <lessons>
        <lesson title="What Are Word and Sentence Embeddings?">
          <key_concepts>
            <concept>Embeddings translate words/sentences into vectors of numbers</concept>
            <concept>Similar words have similar vector representations</concept>
            <concept>Word embeddings capture semantic features (age, size, gender)</concept>
            <concept>Embeddings enable mathematical operations on text (like analogies)</concept>
            <concept>Embeddings assign coordinates in high-dimensional space</concept>
            <concept>Multilingual embeddings can understand meaning across languages</concept>
          </key_concepts>
        </lesson>
        
        <lesson title="What is Similarity Between Sentences?">
          <key_concepts>
            <concept>Dot product similarity multiplies corresponding vector components</concept>
            <concept>Cosine similarity measures the angle between word vectors</concept>
            <concept>Similarity scores are higher for semantically related content</concept>
            <concept>Similar sentences have embeddings that are close in vector space</concept>
            <concept>Normalized embeddings help standardize comparison</concept>
          </key_concepts>
        </lesson>
        
        <lesson title="What Is Attention in Language Models?">
          <key_concepts>
            <concept>Attention helps disambiguate words with multiple meanings</concept>
            <concept>Self-attention weighs the importance of words in context</concept>
            <concept>Words "move closer" to contextually relevant words</concept>
            <concept>Multi-head attention captures different relationship types</concept>
            <concept>Attention enables contextual representations of words</concept>
          </key_concepts>
        </lesson>
        
        <lesson title="What Are Transformer Models and How Do They Work?">
          <key_concepts>
            <concept>Architecture includes tokenization, embedding, positional encoding, and transformer blocks</concept>
            <concept>Models predict next tokens one at a time based on context</concept>
            <concept>Transformers use self-attention to maintain coherence</concept>
            <concept>Softmax layer converts scores to probabilities for token selection</concept>
            <concept>Post-training helps models perform specific tasks</concept>
          </key_concepts>
        </lesson>
      </lessons>
    </module>
    
    <module name="Text Representation">
      <lessons>
        <lesson title="Introduction to Text Embeddings">
          <key_concepts>
            <concept>Embeddings transform unstructured text into structured data</concept>
            <concept>Each dimension represents semantic features of the text</concept>
            <concept>Principal Component Analysis (PCA) can visualize high-dimensional embeddings</concept>
            <concept>Similar texts cluster together in embedding space</concept>
            <concept>Embeddings power applications like search and recommendations</concept>
          </key_concepts>
        </lesson>
      </lessons>
    </module>
  </modules>
  
  <quiz_format>
    <question_count>5</question_count>
    <question_structure>
      <question_text>Clear, unambiguous question testing conceptual understanding</question_text>
      <options>
        <option correct="true">The correct answer</option>
        <option>Plausible but incorrect option</option>
        <option>Plausible but incorrect option</option>
        <option>Plausible but incorrect option</option>
      </options>
      <explanation>Brief explanation of why the correct answer is right</explanation>
    </question_structure>
    <style>
      <tone>Educational, friendly, and accessible</tone>
      <difficulty>Moderate to challenging</difficulty>
      <focus>Conceptual understanding rather than rote memorization</focus>
    </style>
  </quiz_format>
    
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

@sync_to_async
def get_list_of_courses() -> List[Dict[str, str]]:
    """
    Returns a list of all available courses with their IDs, titles, and descriptions.
    """
    courses = Course.objects.all()
    data = [
        {
            "course_id": str(course.id),
            "course_title": course.title,
            "course_description": course.description,
            "category": course.category.name if course.category else "Uncategorized",
            "tags": course.tags,
        }
        for course in courses
    ]
    print("get_list_of_courses", data)
    return data

async def get_course_details(course_id: str) -> Dict[str, Any]:
    """
    Retrieves detailed information about a specific course including modules and their lessons.
    
    Args:
        course_id: The ID of the course to retrieve
        
    Returns:
        Dictionary containing course details, modules, and lessons
    """
    try:
        course = await Course.objects.aget(id=course_id, status=Course.Status.PUBLISHED)
        
        modules_data = []
        for module in course.modules.all().order_by('order'):
            lessons_data = []
            for lesson in module.lessons.all().order_by('order'):
                lesson_data = {
                    "lesson_id": str(lesson.id),
                    "title": lesson.title,
                    "content_type": lesson.get_content_type_display(),
                    "estimated_duration": lesson.estimated_duration,
                    "is_mandatory": lesson.is_mandatory,
                }
                lessons_data.append(lesson_data)
            
            modules_data.append({
                "module_id": str(module.id),
                "title": module.title,
                "description": module.description,
                "lessons": lessons_data
            })
        
        return {
            "course_id": str(course.id),
            "title": course.title,
            "description": course.description,
            "category": course.category.name if course.category else "Uncategorized",
            "tags": course.tags,
            "modules": modules_data
        }
    except Course.DoesNotExist:
        return {"error": f"Course with ID {course_id} not found"}

async def get_lesson_content(lesson_id: str) -> Dict[str, Any]:
    """
    Retrieves the content of a specific lesson.
    
    Args:
        lesson_id: The ID of the lesson to retrieve
        
    Returns:
        Dictionary containing lesson content and metadata
    """
    try:
        lesson = await Lesson.objects.aget(id=lesson_id)
        
        try:
            content = await LessonContent.objects.aget(lesson=lesson)
            content_data = {
                "text_content": content.text_content,
                "embed_code": content.embed_code,
                "external_url": content.external_url,
                "has_file_attachment": bool(content.file_attachment),
                "content_metadata": content.content_metadata
            }
        except LessonContent.DoesNotExist:
            content_data = {"error": "Content for this lesson not found"}
        
        # Check if this lesson has a quiz
        has_quiz = hasattr(lesson, 'quiz')
        
        return {
            "lesson_id": str(lesson.id),
            "title": lesson.title,
            "module": lesson.module.title,
            "course": lesson.module.course.title,
            "content_type": lesson.get_content_type_display(),
            "estimated_duration": lesson.estimated_duration,
            "content": content_data,
            "has_quiz": has_quiz
        }
    except Lesson.DoesNotExist:
        return {"error": f"Lesson with ID {lesson_id} not found"}

async def get_quiz_questions(lesson_id: str) -> Dict[str, Any]:
    """
    Retrieves quiz questions for a specific lesson.
    
    Args:
        lesson_id: The ID of the lesson containing the quiz
        
    Returns:
        Dictionary containing quiz questions and possible answers
    """
    try:
        lesson = await Lesson.objects.aget(id=lesson_id)
        
        if not hasattr(lesson, 'quiz'):
            return {"error": f"No quiz found for lesson with ID {lesson_id}"}
        
        quiz = lesson.quiz
        
        questions_data = []
        for question in quiz.questions.filter(is_active=True).order_by('order'):
            answers_data = []
            for answer in question.answers.all().order_by('order'):
                answers_data.append({
                    "answer_id": str(answer.id),
                    "text": answer.answer_text,
                })
            
            questions_data.append({
                "question_id": str(question.id),
                "text": question.question_text,
                "type": question.get_question_type_display(),
                "explanation": question.explanation,
                "points": question.points,
                "answers": answers_data
            })
        
        return {
            "quiz_id": str(quiz.id),
            "title": quiz.title,
            "description": quiz.description,
            "passing_score": quiz.passing_score,
            "allowed_attempts": quiz.allowed_attempts,
            "randomize_questions": quiz.randomize_questions,
            "time_limit_minutes": quiz.time_limit_minutes,
            "questions": questions_data
        }
    except Lesson.DoesNotExist:
        return {"error": f"Lesson with ID {lesson_id} not found"}

async def generate_quiz_for_lesson(lesson_id: str) -> Dict[str, Any]:
    """
    Generates a new quiz for a lesson using its content.
    
    Args:
        lesson_id: The ID of the lesson to generate a quiz for
        
    Returns:
        Dictionary containing generated quiz questions
    """
    try:
        lesson = await Lesson.objects.aget(id=lesson_id)
        
        try:
            content = await LessonContent.objects.aget(lesson=lesson)
        except LessonContent.DoesNotExist:
            return {"error": "Content for this lesson not found, cannot generate quiz"}
        
        # Here we'd normally use an LLM to generate quiz questions
        # For now, we'll return a placeholder informing that quiz generation is in progress
        
        return {
            "status": "in_progress",
            "message": "Quiz generation has been initiated for lesson: " + lesson.title,
            "lesson_id": str(lesson.id),
            "content_preview": content.text_content[:200] + "..." if len(content.text_content) > 200 else content.text_content
        }
    except Lesson.DoesNotExist:
        return {"error": f"Lesson with ID {lesson_id} not found"}


import os
import json
import datetime
from pathlib import Path

class ChatBotAgent():
    def __init__(
        self,
    ) -> None:
        self.accumulated_text_html = ""
        # Initialize chat history file path
        self.chat_history_dir = Path(settings.BASE_DIR) / "chat_history"
        # Create directory if it doesn't exist
        os.makedirs(self.chat_history_dir, exist_ok=True)
        
    def _get_chat_history_path(self):
        """Generate a unique file path for the chat history"""
        return self.chat_history_dir / f"chat_history.json"
    
    def _save_to_chat_history(self,user_query, llm_response):
        """Save interaction to the chat history JSON file"""
        file_path = self._get_chat_history_path()
        
        # Create timestamp for the interaction
        timestamp = datetime.datetime.now().isoformat()
        
        # Prepare the interaction data
        interaction = {
            "timestamp": timestamp,
            "user_query": user_query,
            "llm_response": llm_response
        }
        
        # Read existing history if file exists
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                history = json.load(f)
        else:
            history = {"interactions": []}
        
        # Append new interaction
        history["interactions"].append(interaction)
        
        # Write updated history back to file
        with open(file_path, 'w') as f:
            json.dump(history, f, indent=2)
            
        return history
    
    def _load_chat_history(self):
        """Load chat history from JSON file"""
        file_path = self._get_chat_history_path()
        
        if not os.path.exists(file_path):
            return {"interactions": []}
        
        with open(file_path, 'r') as f:
            return json.load(f)
    
    def _convert_history_to_messages(self, history):
        """Convert JSON history to chat messages format"""
        messages = []
        
        for interaction in history.get("interactions", []):
            # Add user message
            messages.append(
                ChatMessage(
                    role="user",
                    content=interaction["user_query"]
                )
            )
            
            # Add assistant response
            messages.append(
                ChatMessage(
                    role="assistant",
                    content=interaction["llm_response"]
                )
            )
            
        return messages

    async def execute(self, user_query: str, session_id: str = None):
        try:
                
            # Load chat history
            history_data = self._load_chat_history()

            print(history_data)
            
            self.llm = CustomBedrockConverse(
                aws_access_key_id=settings.BEDROCK_ACCESS_KEY_ID,
                aws_secret_access_key=settings.BEDROCK_SECRET_ACCESS_KEY,
                region_name=settings.BEDROCK_REGION,
                model=CLAUDE_V3_SONNET_MODEL_ID,
                max_tokens=2000,
            )
            
            # Convert history to messages format
            chat_history = self._convert_history_to_messages(history_data)
            
            system_prompt = SYSTEM_PROMPT

            # Pre-fetch course data for the initial state
            courses_list = await get_list_of_courses()
            
            # For efficiency, let's also get the first course details if available
            first_course_details = {}
            if courses_list and len(courses_list) > 0:
                first_course_id = courses_list[0]["course_id"]
                first_course_details = await get_course_details(first_course_id)

            agent_workflow = AgentWorkflow.from_tools_or_functions(
                [
                    get_list_of_courses,
                    get_course_details,
                    get_lesson_content,
                    get_quiz_questions,
                    generate_quiz_for_lesson,
                ],
                llm=self.llm,
                system_prompt=system_prompt,
                initial_state={
                    "user_query": user_query,
                    "available_courses_to_user": courses_list,
                    "first_course_details": first_course_details,
                    "course_count": len(courses_list),
                    "chat_history": history_data,
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
            
            # Save the completed interaction to chat history
            if soup and soup.answer and soup.answer.text.strip():
                # Save the conversation to the JSON file
                self._save_to_chat_history(
                    user_query=user_query,
                    llm_response=soup.answer.text.strip()
                )

            last_chunk = {
                "id": message_id,
                "accumulated_text": self.accumulated_text_html,
                "chunk_text": "",
                "total_chunk_count": chunk_count,
                "response_stream_end": True,
                "error": False,
                "session_id": session_id  # Include session ID in the response
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