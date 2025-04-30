from typing import Optional
from pydantic import BaseModel

class RoleCreate(BaseModel):
    role_name: str
    role_description: str
    can_create_files: bool
    can_create_folders: bool


class RoleUpdate(BaseModel):
    role_name: Optional[str] = None
    role_description: Optional[str] = None
    can_create_files: Optional[bool] = None
    can_create_folders: Optional[bool] = None


class RoleResponse(BaseModel):
    role_id: int
    role_name: str
    role_description: str
    can_create_files: bool
    can_create_folders: bool

    class Config:
        from_attributes = True
