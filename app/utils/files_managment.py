import os
import urllib.parse
from typing import Optional
from fastapi import APIRouter
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from fastapi import UploadFile, HTTPException

load_dotenv()
s3_bucket_name = os.getenv("S3_BUCKET")
aws_region = os.getenv("AWS_REGION", "us-east-2")


def create_s3_url(file_name: str) -> str:
    """This function is used to create S3 URL.

    Args:
        file_name (str): The name of the file.

    Returns:
        str: The S3 URL of the uploaded file.
    """

    safe_chars = (
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._~,:;/=?& ()"
    )
    encoded_file_name = urllib.parse.quote(file_name, safe=safe_chars)
    return f"https://{s3_bucket_name}.s3.{aws_region}.amazonaws.com/{encoded_file_name.replace(' ', '+')}"


async def prepare_data_for_db(uploaded_file: UploadFile, folder_id: int, owner_id: int) -> dict:
    """This function is used to get data-file to db.

    Args:
        uploaded_file (UploadFile): The uploaded file.
        s3_url (str): The S3 URL of the uploaded file.
        folder_id (int): The folder ID where the file is stored.

    Returns:
        dict: A dictionary containing file information.

    Raises:
        HTTPException: If there is an error while processing the file.
    """
    try:

        await uploaded_file.seek(0)
        file_metadata = {
            "size": f"{len(await uploaded_file.read()) / 1024:.2f}kb",
        }
        await uploaded_file.seek(0)

        response = {
            "file_name": (os.path.splitext(uploaded_file.filename)[0]),
            "file_metadata": file_metadata,
            "file_type": os.path.splitext(uploaded_file.filename)[1],
            "folder_id": folder_id,
            "owner_id": owner_id,
            "s3_url": create_s3_url(uploaded_file.filename),
        }

        return response

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def save_file_temporarily(uploaded_file: UploadFile) -> str:
    """This function is used to save the file temporarily.

    Args:
        uploaded_file (UploadFile): The uploaded file.

    Returns:
        str: The path of the temporarily saved file.

    Raises:
        HTTPException: If there is an error while saving the file.
    """
    try:
        temp_file_path = f"/tmp/{uploaded_file.filename}"
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.file.read())
        return temp_file_path
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
