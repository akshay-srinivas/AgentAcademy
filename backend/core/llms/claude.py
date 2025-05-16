import json
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Sequence,
    Tuple,
)

from llama_index.core.llms import (
    ChatMessage,
    ChatResponse,
    ChatResponseAsyncGen,
    MessageRole,
)
from llama_index.core.llms.callbacks import llm_chat_callback
from llama_index.llms.bedrock_converse import BedrockConverse
from llama_index.llms.bedrock_converse.utils import (
    converse_with_retry_async,
    join_two_dicts,
    messages_to_converse_messages,
)

from agentacademy.settings import (
    BEDROCK_ACCESS_KEY_ID,
    BEDROCK_REGION,
    BEDROCK_SECRET_ACCESS_KEY,
)
from core.llms.constants import (
    CLAUDE_V3_5_HAIKU_MODEL_ID,
    DEFAULT_CLAUDE_MAX_TOKENS_TO_SAMPLE,
)


def get_claude_llm() -> BedrockConverse:
    return CustomBedrockConverse(
        aws_access_key_id=BEDROCK_ACCESS_KEY_ID,
        aws_secret_access_key=BEDROCK_SECRET_ACCESS_KEY,
        region_name=BEDROCK_REGION,
        model=CLAUDE_V3_5_HAIKU_MODEL_ID,
        max_tokens=DEFAULT_CLAUDE_MAX_TOKENS_TO_SAMPLE,
    )


class CustomBedrockConverse(BedrockConverse):
    def _get_content_and_tool_calls(
        self, response: Optional[Dict[str, Any]] = None, content: Dict[str, Any] = None
    ) -> Tuple[str, Dict[str, Any], List[str], List[str]]:
        assert (
            response is not None or content is not None
        ), f"Either response or content must be provided. Got response: {response}, content: {content}"
        assert (
            response is None or content is None
        ), f"Only one of response or content should be provided. Got response: {response}, content: {content}"
        tool_calls = []
        tool_call_ids = []
        status = []
        text_content = ""
        if content is not None:
            content_list = [content]
        else:
            content_list = response["output"]["message"]["content"]
        for content_block in content_list:
            if text := content_block.get("text", None):
                text_content += text
            if tool_usage := content_block.get("toolUse", None):
                if tool_usage.get("input"):
                    input = tool_usage["input"]
                    try:
                        json.loads(input)
                        tool_usage["input"] = json.loads(input)
                        tool_calls.append(tool_usage)
                    except json.JSONDecodeError:
                        pass
            if tool_result := content_block.get("toolResult", None):
                for tool_result_content in tool_result["content"]:
                    if text := tool_result_content.get("text", None):
                        text_content += text
                tool_call_ids.append(tool_result_content.get("toolUseId", ""))
                status.append(tool_result.get("status", ""))

        return text_content, tool_calls, tool_call_ids, status

    @llm_chat_callback()
    async def astream_chat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponseAsyncGen:
        # convert Llama Index messages to AWS Bedrock Converse messages
        converse_messages, system_prompt = messages_to_converse_messages(messages)
        if len(system_prompt) > 0 or self.system_prompt is None:
            self.system_prompt = system_prompt
        all_kwargs = self._get_all_kwargs(**kwargs)

        # invoke LLM in AWS Bedrock Converse with retry
        response_gen = await converse_with_retry_async(
            session=self._asession,
            config=self._config,
            messages=converse_messages,
            system_prompt=self.system_prompt,
            max_retries=self.max_retries,
            stream=True,
            guardrail_identifier=self.guardrail_identifier,
            guardrail_version=self.guardrail_version,
            trace=self.trace,
            **all_kwargs,
        )

        async def gen() -> ChatResponseAsyncGen:
            content = {}
            role = MessageRole.ASSISTANT
            async for chunk in response_gen:
                if content_block_delta := chunk.get("contentBlockDelta"):
                    content_delta = content_block_delta["delta"]
                    content = join_two_dicts(content, content_delta)
                    (
                        _,
                        tool_calls,
                        tool_call_ids,
                        status,
                    ) = self._get_content_and_tool_calls(content=content)

                    yield ChatResponse(
                        message=ChatMessage(
                            role=role,
                            content=content.get("text", ""),
                            additional_kwargs={
                                "tool_calls": tool_calls,
                                "tool_call_id": tool_call_ids,
                                "status": status,
                            },
                        ),
                        delta=content_delta.get("text", ""),
                        raw=chunk,
                    )
                elif content_block_start := chunk.get("contentBlockStart"):
                    tool_use = content_block_start["start"]
                    content = join_two_dicts(content, tool_use)
                    (
                        _,
                        tool_calls,
                        tool_call_ids,
                        status,
                    ) = self._get_content_and_tool_calls(content=content)

                    yield ChatResponse(
                        message=ChatMessage(
                            role=role,
                            content=content.get("text", ""),
                            additional_kwargs={
                                "tool_calls": tool_calls,
                                "tool_call_id": tool_call_ids,
                                "status": status,
                            },
                        ),
                        raw=chunk,
                    )

        return gen()
