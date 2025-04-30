from typing import Optional, Any
from datetime import datetime
from pydantic import BaseModel


class FileCreate(BaseModel):
    file_name: str
    file_metadata: dict[str, Any]
    file_type: str
    folder_id: int
    owner_id: int
    s3_url: str


class FileUpdate(BaseModel):
    file_name: Optional[str] = None
    file_metadata: Optional[dict[str, Any]] = None
    file_type: Optional[str] = None
    folder_id: Optional[int] = None
    owner_id: Optional[int] = None
    s3_url: Optional[str] = None


class FileResponse(BaseModel):
    file_id: int
    file_name: str
    file_metadata: dict[str, Any]
    file_type: str
    folder_id: int
    owner_id: int
    s3_url: str
    uploaded_at: datetime

    class Config:
        from_attributes = True
