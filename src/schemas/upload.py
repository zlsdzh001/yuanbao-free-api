from pydantic import BaseModel, Field


class File(BaseModel):
    file_name: str
    file_data: str
    file_type: str = Field(..., pattern="^(image|doc)$")


class UploadFileRequest(BaseModel):
    agent_id: str
    hy_source: str = "web"
    hy_user: str
    file: File
