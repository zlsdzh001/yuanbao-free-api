from typing import Optional

from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sse_starlette.sse import EventSourceResponse

from src.schemas import ChatCompletionRequest, YuanBaoChatCompletionRequest
from src.services import create_completion_stream, create_conversation
from src.utils import generate_headers, get_model_info, parse_messages

app = FastAPI()

bearer_scheme = HTTPBearer(auto_error=False)

HTTP_STATUS_UNAUTHORIZED = 401
HTTP_STATUS_BAD_REQUEST = 400
HTTP_STATUS_ERROR = 500


def error_response(status_code: int, message: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"status": status_code, "message": message},
    )


@app.post("/v1/chat/completions")
async def chat_completions(
    request: ChatCompletionRequest, authorization: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme)
):
    try:
        if not authorization or not authorization.credentials:
            return error_response(HTTP_STATUS_UNAUTHORIZED, "need token")

        token = authorization.credentials
        headers = generate_headers(request, token)
        if request.chat_id is None or request.chat_id == "":
            try:
                request.chat_id = await create_conversation(request.agent_id, headers)
            except Exception as e:
                return error_response(HTTP_STATUS_BAD_REQUEST, f"create conversation failed: {str(e)}")

        prompt = parse_messages(request.messages)
        model_info = get_model_info(request.model)
        chat_request = YuanBaoChatCompletionRequest(
            agent_id=request.agent_id,
            chat_id=request.chat_id,
            prompt=prompt,
            chat_model_id=model_info["model"],
            support_functions=model_info["support_functions"],
        )

        try:
            generator = create_completion_stream(chat_request, headers, request.should_remove_conversation)
            return EventSourceResponse(generator, media_type="text/event-stream")
        except Exception as e:
            return error_response(HTTP_STATUS_BAD_REQUEST, f"stream generation failed: {str(e)}")

    except Exception as e:
        return error_response(HTTP_STATUS_ERROR, f"internal server error: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
