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
#from models.model import File as FileModel
from schemas.file_schema import FileCreate, FileUpdate, FileResponse
from utils.files_managment import (
    save_file_temporarily,
    prepare_data_for_db,
)

load_dotenv()
s3_bucket_name = os.getenv("S3_BUCKET")

router = APIRouter()

@router.get("/get-files/", response_model=List[FileResponse])
def get_all_files(db: Session = Depends(get_db)):
    """Get all files from the database.
    
    Args:
        db (Session): SQLAlchemy session object
        
    Returns:
        List[File]: a list of File objects
        
    Raises:
        HTTPException: If there is an error during the retrieval.
    """
    try:
        all_files = files_services.get_all_files(db)
        if not all_files:
            raise HTTPException(status_code=404, detail="No files found")

        return all_files
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")

@router.get("/get-files-user-id/{user_id}", response_model=List[FileResponse])
def get_files_by_user_id(user_id: int, db: Session = Depends(get_db)):
    """Get all files owned by a specific user.

    Args:
        user_id (int): ID of the user whose files to retrieve
        db (Session): SQLAlchemy session object

    Returns:
        List[File]: List of File objects owned by the user

    Raises:
        HTTPException: If there is an error during the retrieval.
    """
    try:
        user_files = files_services.get_files_by_user_id(db, user_id)

        if not user_files:
            raise HTTPException(status_code=404, detail="No files found for this user")

        return user_files

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")


@router.get("/get-file-name/{file_name}", response_model=FileResponse)
def get_file_by_name_in_db(file_name: str, db: Session = Depends(get_db)):
    """This function is used to get a file by its name from the database.

    Args:
        file_name (str): The name of the file to be retrieved.
        db (Session): SQLAlchemy session object.

    Returns:
        FileResponse: The file data if found.

    Raises:
        HTTPException: If the file is not found in the database.
        HTTPException: If there is an error during the retrieval.
    """
    try:
        file_data = files_services.get_file_by_name_in_db(db, file_name)

        if not file_data:
            raise HTTPException(status_code=404, detail="File not found")

        return file_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving file: {str(e)}")



@router.post("/upload-register-file", response_model=FileResponse)
async def upload_and_register_file(
    uploaded_file: UploadFile = File(...),
    folder_id: int = Form(1),
    owner_id: int = Form(1),
    db: Session = Depends(get_db),
):
    """This function first registers the file in the database and then uploads the file to S3.

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
            uploaded_file=uploaded_file, folder_id=folder_id, owner_id=owner_id, db=db
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
    owner_id: int = Form(1),
    db: Session = Depends(get_db),
):
    """This function is used to register a file in the database.

    Args:
        uploaded_file (UploadFile): The uploaded file.
        folder_id (int): The folder ID where the file is categorized.
        owner_id (int): The ID of the owner of the file.
        db (Session): SQLAlchemy session object.

    Returns:
        JSONResponse: A response indicating success or failure.

    Raises:
        HTTPException: If there is an error during the registration.
    """
    try:
        data_to_save_db = await prepare_data_for_db(uploaded_file, folder_id, owner_id)

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
    """This function is used to upload a file to S3.

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

    except Exception:
        raise HTTPException(status_code=500, detail=f"Failed to upload file: {str(e)}")


@router.delete("/delete-file/{file_id}/{file_name}/{user_id}")
def delete_file(
    file_id: int, file_name: str, user_id: int, db: Session = Depends(get_db)
):
    """
    Delete a file from the database and S3. If deletion from S3 fails, restore DB record.

    Args:
        file_id (int): ID of the file to delete.
        file_name (str): Name of the file.
        user_id (int): ID of the user requesting deletion.
        db (Session): DB session.

    Returns:
        JSONResponse
    """
    try:
        file = files_services.get_file_by_name_in_db(db, file_name)
        if file is None:
            raise HTTPException(status_code=404, detail="File not found in database")

        if file.file_id != file_id:
            raise HTTPException(status_code=400, detail="File ID and name do not match")

        file_backup = {
            "file_name": file.file_name,
            "file_metadata": file.file_metadata,
            "file_type": file.file_type,
            "folder_id": file.folder_id,
            "owner_id": file.owner_id,
            "s3_url": file.s3_url,
            "uploaded_at": file.uploaded_at,
        }
        file_name_extension = f"{file_backup['file_name']}{file_backup['file_type']}"
        
        result, message = files_services.delete_file_from_db(db, file_id, user_id)
        if result <= 0:
            raise HTTPException(status_code=403 if result == 0 else 500, detail=message)

        s3_result = files_services.delete_file_from_s3(
            db, s3_bucket_name, file_name_extension.strip()
        )
        if s3_result is None:
            try:
                restored_file = File(**file_backup)
                db.add(restored_file)
                db.commit()

            except Exception as e:
                db.rollback()
                raise HTTPException(
                    status_code=500,
                    detail=f"Error restoring file in DB after S3 deletion failure: {str(e)}",
                )

            raise HTTPException(
                status_code=500,
                detail="Error deleting file from S3. File restored in DB.",
            )
            
        return JSONResponse(
            status_code=200,
            content={"message": "File deleted successfully"},
        )

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.delete("/delete-file-from-db/{file_id}/{user_id}")
def delete_file_fom_db(file_id: int, user_id, db: Session = Depends(get_db)):
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
        flag = files_services.delete_file_from_db(db, file_id, user_id)

        if flag[0] == 0:
            raise HTTPException(status_code=404, detail=f"{flag[1]}")
        elif flag[0] == -1:
            raise HTTPException(status_code=500, detail=f"{flag[1]}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting file. {str(e)}")


@router.delete("/delete-file-from-s3/{file_name}")
def delete_file_fom_s3(file_name: str, db: Session = Depends(get_db)):
    """This function is used to delete a file from S3.

    Args:
        file_name (str): The name of the file to be deleted.

    Returns:
        JSONResponse: A response indicating success or failure.

    Raises:
        HTTPException: If there is an error during the deletion.
        HTTPException: If the file is not found in S3.
    """

    try:
        response = files_services.delete_file_from_s3(
            db, s3_bucket_name, file_name.strip()
        )

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
