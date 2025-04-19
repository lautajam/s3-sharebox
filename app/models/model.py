from sqlalchemy import Column, Integer, String, Boolean, JSON, DateTime
from app.database import Base
from datetime import datetime, timezone

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    username = Column(String)
    password = Column(String)
    role_id = Column(Integer)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    role_name =  Column(String)
    role_description = Column(String)
    can_create_files = Column(Boolean)
    can_create_folders = Column(Boolean)

class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    tag_name = Column(String)
    tag_description = Column(String)
    
class Folder(Base):
    __tablename__ = "folders"
    id = Column(Integer, primary_key=True)
    folder_name = Column(String)
    parent_folder_id = Column(Integer)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
class File(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True)
    file_name = Column(String)
    file_metadata = Column(JSON)
    file_type = Column(String)
    folder_id = Column(Integer)
    uploaded_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
class FileTag(Base):
    __tablename__ = "file_tags"
    file_id = Column(Integer, primary_key=True)
    tag_id = Column(Integer, primary_key=True)
    
class FolderTag(Base):
    __tablename__ = "folder_tags"
    folder_id = Column(Integer, primary_key=True)
    tag_id = Column(Integer, primary_key=True)
    
class FolderRole(Base):
    __tablename__ = "folder_roles"
    folder_id = Column(Integer, primary_key=True)
    role_id = Column(Integer, primary_key=True)
    access_level = Column(String)
    
class FileRole(Base):
    __tablename__ = "file_roles"
    file_id = Column(Integer, primary_key=True)
    role_id = Column(Integer, primary_key=True)
    access_level = Column(String)
