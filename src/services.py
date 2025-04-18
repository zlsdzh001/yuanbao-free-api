from typing import AsyncGenerator, Dict

import httpx

from src.schemas import YuanBaoChatCompletionRequest
from src.utils import process_response_stream

CREATE_URL = "https://yuanbao.tencent.com/api/user/agent/conversation/create"
CLEAR_URL = "https://yuanbao.tencent.com/api/user/agent/conversation/v1/clear"
CHAT_URL = "https://yuanbao.tencent.com/api/chat/{}"

DEFAULT_TIMEOUT = 60


class ConversationCreationError(Exception):
    pass


class ConversationRemoveError(Exception):
    pass


class ChatCompletionError(Exception):
    pass


async def create_conversation(agent_id: str, headers: Dict[str, str], timeout: float = DEFAULT_TIMEOUT) -> str:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(CREATE_URL, json={"agentId": agent_id}, headers=headers, timeout=timeout)

            if response.status_code != 200:
                raise Exception(f"Request failed. Status code: {response.status_code}, Response: {response.text}")

            try:
                json_data = response.json()
            except ValueError:
                raise Exception(f"Failed to parse response as JSON. Response: {response.text}")

            if "id" not in json_data:
                raise Exception(f"Failed to find 'id' in response JSON. Response: {response.text}")

            return json_data["id"]

    except Exception as e:
        raise ConversationCreationError(e)


async def remove_conversation(chat_id: str, headers: Dict[str, str], timeout: float = DEFAULT_TIMEOUT) -> None:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                CLEAR_URL,
                json={"conversationIds": [chat_id], "uiOptions": {"noToast": True}},
                headers=headers,
                timeout=timeout,
            )

            if response.status_code != 200:
                raise Exception(f"Request failed. Status code: {response.status_code}, Response: {response.text}")

    except Exception as e:
        raise ConversationRemoveError(e)


async def create_completion_stream(
    chat_request: YuanBaoChatCompletionRequest,
    headers: Dict[str, str],
    should_remove_conversation: bool = False,
    timeout: float = DEFAULT_TIMEOUT,
) -> AsyncGenerator[str, None]:
    body = {
        "model": "gpt_175B_0404",
        "prompt": chat_request.prompt,
        "plugin": "Adaptive",
        "displayPrompt": chat_request.prompt,
        "displayPromptType": 1,
        "options": {"imageIntention": {"needIntentionModel": True, "backendUpdateFlag": 2, "intentionStatus": True}},
        "multimedia": [],
        "agentId": chat_request.agent_id,
        "supportHint": 1,
        "version": "v2",
        "chatModelId": chat_request.chat_model_id,
    }
    if chat_request.support_functions:
        body["supportFunctions"] = chat_request.support_functions

    try:
        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST",
                CHAT_URL.format(chat_request.chat_id),
                json=body,
                headers=headers,
                timeout=timeout,
            ) as response:
                async for chunk in process_response_stream(response, chat_request.chat_id):
                    yield chunk

    except Exception as e:
        raise ChatCompletionError(e)

    finally:
        if should_remove_conversation:
            await remove_conversation(chat_request.chat_id, headers)
