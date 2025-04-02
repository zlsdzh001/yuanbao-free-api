from typing import AsyncGenerator, Dict

import httpx

from src.schemas import YuanBaoChatCompletionRequest
from src.utils import process_response_stream

CREATE_URL = "https://yuanbao.tencent.com/api/user/agent/conversation/create"
CLEAR_URL = "https://yuanbao.tencent.com/api/user/agent/conversation/v1/clear"
CHAT_URL = "https://yuanbao.tencent.com/api/chat/{}"


async def create_conversation(agent_id: str, headers: Dict[str, str]) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(CREATE_URL, json={"agentId": agent_id}, headers=headers)

        json_data = response.json()
        return json_data["id"]


async def remove_conversation(chat_id: str, headers: Dict[str, str]) -> None:
    async with httpx.AsyncClient() as client:
        await client.post(
            CLEAR_URL,
            json={"conversationIds": [chat_id], "uiOptions": {"noToast": True}},
            headers=headers,
        )


async def create_completion_stream(
    chat_request: YuanBaoChatCompletionRequest, headers: Dict[str, str], should_remove_conversation: bool = False
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

    async with httpx.AsyncClient() as client:
        async with client.stream(
            "POST",
            CHAT_URL.format(chat_request.chat_id),
            json=body,
            headers=headers,
        ) as response:
            async for chunk in process_response_stream(response, chat_request.chat_model_id):
                yield chunk

    if should_remove_conversation:
        await remove_conversation(chat_request.chat_id, headers)
