import os
import json
import urllib.parse
from typing import List
from database import get_db
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form

from services import files_services
from schemas.file_schema import FileCreate, FileUpdate, FileResponse
from utils.files_managment import (
    save_file_temporarily,
    prepare_data_for_db,
)

load_dotenv()
s3_bucket_name = os.getenv("S3_BUCKET")

router = APIRouter()


@router.post("/upload-register-file", response_model=FileResponse)
async def upload_and_register_file(
    uploaded_file: UploadFile = File(...),
    folder_id: int = Form(1),
    db: Session = Depends(get_db),
):
    """ This function first registers the file in the database and then uploads the file to S3.

    Args:
        uploaded_file (UploadFile): The uploaded file.
        folder_id (int): The folder ID where the file is categorized.
        db (Session): SQLAlchemy session object.

    Returns:
        JSONResponse: A response indicating success or failure.

    Raises:
        HTTPException: If there is an error during the upload or database operation.
    """
    try:
        # Luego subir a S3
        await upload_file_to_s3(uploaded_file=uploaded_file)

        # Primero registrar en DB
        await register_file_in_db(
            uploaded_file=uploaded_file, folder_id=folder_id, db=db
        )

        return JSONResponse(
            status_code=201,
            content={
                "message": "File registered in DB and uploaded to S3 successfully"
            },
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to register and upload file: {str(e)}"
        )


@router.post("/register-file-in-db", response_model=FileResponse)
async def register_file_in_db(
    uploaded_file: UploadFile = File(...),
    folder_id: int = Form(1),
    db: Session = Depends(get_db),
):
    """ This function is used to register a file in the database.

    Args:
        uploaded_file (UploadFile): The uploaded file.
        folder_id (int): The folder ID where the file is categorized.
        db (Session): SQLAlchemy session object.

    Returns:
        JSONResponse: A response indicating success or failure.

    Raises:
        HTTPException: If there is an error during the registration.
    """
    try:
        data_to_save_db = await prepare_data_for_db(uploaded_file, folder_id)

        file_data = FileCreate(**data_to_save_db)
        files_services.create_file_to_db(db, file_data)

        return JSONResponse(
            status_code=201,
            content={"message": "File registered in database successfully"},
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to register file: {str(e)}"
        )


@router.post("/upload-file-to-s3")
async def upload_file_to_s3(
    uploaded_file: UploadFile = File(...),
):
    """ This function is used to upload a file to S3.

    Args:
        uploaded_file (UploadFile): The uploaded file.

    Returns:
        JSONResponse: A response indicating success or failure.

    Raises:
        HTTPException: If there is an error during the upload.
    """
    try:
        temp_file_path = save_file_temporarily(uploaded_file)

        is_upload = files_services.upload_file_to_s3(
            temp_file_path,
            s3_bucket_name,
            uploaded_file.filename,
        )

        if is_upload is not True:
            raise HTTPException(status_code=500, detail="Failed to upload file to S3.")

        return JSONResponse(
            status_code=201,
            content={"message": "File uploaded to S3 successfully"},
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload file: {str(e)}")


@router.delete("/delete-file/{file_id}/{file_name}")
def delete_file(file_id: int, file_name: str, db: Session = Depends(get_db)):
    """ This function is used to delete a file from S3 and the database.

    Args:
        file_id (int): The ID of the file to be deleted.
        file_name (str): The name of the file to be deleted.

    Returns:
        JSONResponse: A response indicating success or failure.

    Raises:
        HTTPException: If there is an error during the deletion.
        HTTPException: If the file is not found in the database.
    """
    try:

        # Hay que hacer un chequeo de que el file_name sea del file_id

        # Eliminar de S3
        delete_file_fom_s3(file_name)

        # Eliminar de la base de datos
        delete_file_fom_db(file_id, db)

        return JSONResponse(
            status_code=200,
            content={"message": "File deleted successfully from S3 and database"},
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting file: {str(e)}")


@router.delete("/delete-file-from-db/{file_id}")
def delete_file_fom_db(file_id: int, db: Session = Depends(get_db)):
    """This function is used to delete a file from the database.

    Args:
        file_id (int): The ID of the file to be deleted.
        db (Session): SQLAlchemy session object.

    Returns:
        JSONResponse: A response indicating success or failure.

    Raises:
        HTTPException: If there is an error during the deletion.
        HTTPException: If the file is not found in the database.
    """

    try:
        flag = files_services.delete_file_from_db(db, file_id)

        if flag[0] == 0:
            raise HTTPException(status_code=404, detail=f"{flag[1]}")
        elif flag[0] == -1:
            raise HTTPException(status_code=500, detail=f"{flag[1]}")

        return JSONResponse(
            status_code=200,
            content={"message": f"flag[1]"},
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting file. {str(e)}")


@router.delete("/delete-file-from-s3/{file_name}")
def delete_file_fom_s3(file_name: str):
    """ This function is used to delete a file from S3.
    
    Args:
        file_name (str): The name of the file to be deleted.
        
    Returns:
        JSONResponse: A response indicating success or failure.
        
    Raises:
        HTTPException: If there is an error during the deletion.
        HTTPException: If the file is not found in S3.
    """

    try:
        response = files_services.delete_file_from_s3(s3_bucket_name, file_name.strip())

        if response is None:
            return JSONResponse(
                status_code=500,
                content={"message": "Error deleting file."},
            )

        return JSONResponse(
            status_code=200,
            content={"message": "File deleted successfully"},
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting file. {str(e)}")


""" Old upload function
@router.post("/upload-register-file", response_model=FileResponse)
async def upload_file(
    uploaded_file: UploadFile = File(...),
    folder_id: int = Form(1),  # Hay que cambiar esto cuando se implementen las carpetas
    db: Session = Depends(get_db),
):
   This function is used to upload a file to S3 and register it in the database.

    Args:
        uploaded_file (UploadFile): The uploaded file.
        db (Session): SQLAlchemy session object.

    Returns:
        JSONResponse: A response indicating success or failure.

    Raises:
        HTTPException: If there is an error during the upload or database operation.
 
    try:

        temp_file_path = save_file_temporarily(uploaded_file)

        data_to_save_db = await prepare_data_for_db(uploaded_file, folder_id)

        try:
            file_data = FileCreate(**data_to_save_db)
            files_services.create_file_to_db(db, file_data)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail="Failed to register file in database. " + str(e)
            )

        is_upload = files_services.upload_file_to_s3(
            temp_file_path,
            s3_bucket_name,
            uploaded_file.filename,
        )

        if is_upload is not True:
            # Hay que eliminarlo de la db
            # files_services.delete_file_from_db(db, file_data.id)
            raise HTTPException(status_code=500, detail="Failed to upload file to S3.")

        return JSONResponse(
            status_code=201,
            content={"message": "File uploaded and registered successfully"},
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))"""
