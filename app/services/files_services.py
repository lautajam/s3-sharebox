import os
import boto3
from typing import Tuple
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

from models.model import File, User
from schemas.file_schema import FileCreate, FileUpdate

load_dotenv()
aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region = os.getenv("AWS_REGION")

ADMIN_ROLE_ID = 1

def get_file_by_name_in_s3(db: Session, file_name: str, aws_bucket_name: str) -> File:
    """Get a file from S3 bucket by its name.
    
    Args:
        db (Session): SQLAlchemy session object
        file_name (str): Name of the file to retrieve
        aws_bucket_name (str): S3 bucket name
        
    Returns:
        File: File object if found, None otherwise
    """
    s3 = boto3.client("s3")

    try:
        response = s3.list_objects_v2(Bucket=aws_bucket_name, Prefix=file_name)
        return response
    except Exception as e:
        return None

def get_file_by_name_in_db(db: Session, file_name: str) -> File:
    """Get a file from the database by its name.

    Args:
        db (Session): SQLAlchemy session object
        file_name (str): Name of the file to retrieve

    Returns:
        File: File object if found, None otherwise
    """
    return db.query(File).filter(File.file_name == file_name).first()

def upload_file_to_s3(file_path, bucket_name, s3_file_name) -> bool:
    """
    Upload a file to an S3 bucket with optional extra parameters.

    Args:
        file_path (str): Local path to the file.
        bucket_name (str): S3 bucket name.
        s3_file_name (str): Name to save the file as in S3.

    Returns:
        str: URL of the uploaded file in S3 or None if upload fails.
    """
    s3 = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region,
    )

    try:
        s3.upload_file(file_path, bucket_name, s3_file_name)
        return True
    except Exception as e:
        return False


def create_file_to_db(db: Session, new_file_data: FileCreate):
    """Create a new file in the database.

    Args:
        db (Session): SQLAlchemy session object
        new_file_data (FileCreate): File data to be created

    Returns:
        File: Created File object
    """

    new_file = File(**new_file_data.dict())

    db.add(new_file)
    db.commit()
    db.refresh(new_file)
    return new_file


def delete_file_from_db(db: Session, file_id: int, user_id: int) -> Tuple[int, str]:
    """Delete a file from the database.

    Args:
        db (Session): SQLAlchemy session object
        file_id (int): ID of the file to be deleted

    Returns:
        bool: True if deletion was successful, False otherwise
    """

    try:
        is_user_owner = db.query(File).filter(File.file_id == file_id, File.owner_id == user_id).first()
        is_admin = db.query(User).filter(User.user_id == user_id, User.role_id == ADMIN_ROLE_ID).first()
        if not (is_user_owner or is_admin):
            return (0, "You are not the owner of this file or an admin")
        
        file_to_delete = db.query(File).filter(File.file_id == file_id).first()
        if not file_to_delete:
            return (0, "File not found")

        db.delete(file_to_delete)
        db.commit()
        return (1, "File deleted successfully")
    except Exception as e:
        return (-1, f"Error deleting file. {str(e)}")


def delete_file_from_s3(db: Session, s3_bucket_name: str, file_name: str) -> str:
    """Delete a file from S3 bucket.
    
    Args:
        db (Session): SQLAlchemy session object
        s3_bucket_name (str): S3 bucket name
        file_name (str): Name of the file to be deleted
        
    Returns:
        str: Response from S3 delete operation or None if file not found
    """
    
    file = get_file_by_name_in_db(db, file_name)
    if file is not None:
        file_type = file.file_type if file else None
        
        file_name = f"{file_name}{file_type}"
    s3 = boto3.client("s3")

    try:
        response = s3.delete_object(Bucket=s3_bucket_name, Key=file_name)
        return response
    except Exception as e:
        return None
