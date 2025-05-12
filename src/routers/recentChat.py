import logging

from fastapi.responses import JSONResponse

from fastapi import APIRouter, Depends

from src.dependencies.auth import get_authorized_headers

router = APIRouter()

ShareChat = {}

def newResponse(status_code: int, message: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"status": status_code, "message": message},
    )

@router.get("/v1/recent/chat")
def chat_completions(
    hy_user:str, 
    headers: dict = Depends(get_authorized_headers),
):
    try:
        if not hy_user:
            return newResponse(400, "need hy_user")
        if hy_user in ShareChat:
            return newResponse(200, ShareChat[hy_user])
        else:
            return newResponse(200, "hy_user not found")
    except Exception as e:
        logging.error(f"Internal server error: {str(e)}", exc_info=True)
        return newResponse(500, f"internal server error: {str(e)}")

@router.delete("/v1/recent/chat")
def chat_completions(
    hy_user:str,
    headers: dict = Depends(get_authorized_headers),
):
    try:
        if not hy_user:
            return newResponse(400, "need hy_user")
        if hy_user in ShareChat:
            ShareChat.pop(hy_user)
            return newResponse(200, "success")
        else:
            return newResponse(400, "hy_user not found")
    except Exception as e:
        logging.error(f"Internal server error: {str(e)}", exc_info=True)
        return newResponse(500, f"internal server error: {str(e)}")