import os
import boto3
from models.model import File
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from schemas.file_schema import FileCreate, FileUpdate

load_dotenv()
aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region = os.getenv("AWS_DEFAULT_REGION")

#def get_all_files_at_db(db: Session):
#    return db.query(File).all()

def upload_file_to_s3(file_path, bucket_name, s3_file_name) -> str:
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
    
    print(f"Uploading {file_path} to bucket {bucket_name} as {s3_file_name}")
    print(f"Key: {aws_access_key}")
    print(f"Secret: {aws_secret_key}")
    
    try:
        s3.upload_file(file_path, bucket_name, s3_file_name)
            
        s3_url = f"https://{bucket_name}.s3.amazonaws.com/{s3_file_name}"
        return s3_url
    except Exception as e:
        return None

    
def create_file_at_db(db: Session, new_file_data: FileCreate):
    """ Create a new file in the database.
    
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