import os
import boto3
from typing import Tuple
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

from models.model import File
from schemas.file_schema import FileCreate, FileUpdate

load_dotenv()
aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region = os.getenv("AWS_REGION")


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


def delete_file_from_db(db: Session, file_id: int) -> Tuple[int, str]:
    """Delete a file from the database.

    Args:
        db (Session): SQLAlchemy session object
        file_id (int): ID of the file to be deleted

    Returns:
        bool: True if deletion was successful, False otherwise
    """
    try:
        file_to_delete = db.query(File).filter(File.file_id == file_id).first()
        if not file_to_delete:
            return (0, "File not found")

        db.delete(file_to_delete)
        db.commit()
        return (1, "File deleted successfully")
    except Exception as e:
        return (-1, f"Error deleting file. {str(e)}")


def delete_file_from_s3(s3_bucket_name: str, file_name: str) -> dict|str:
    """
    
    """

    s3 = boto3.client("s3")

    try:
        response = s3.delete_object(Bucket=s3_bucket_name, Key=file_name)
        return response
    except Exception as e:
        return None
