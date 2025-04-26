import os
import json
from typing import List
from database import get_db
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form

from services import files_services
from schemas.file_schema import FileCreate, FileUpdate, FileResponse

load_dotenv()
s3_bucket_name = os.getenv("S3_BUCKET")

router = APIRouter()


@router.get("/get-files", response_model=FileResponse)
def get_all_users(db: Session = Depends(get_db)):
    pass


@router.post("/create-file", response_model=FileResponse)
def upload_file(
    uploaded_file: UploadFile = File(...),
    new_file: str = Form(...),
    db: Session = Depends(get_db),
):
    try:
        # Guardar el archivo temporalmente
        temp_file_path = f"/tmp/{uploaded_file.filename}"
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.file.read())

        new_file_dict = json.loads(new_file)

        s3_url = files_services.upload_file_to_s3(
            temp_file_path,
            s3_bucket_name,
            new_file_dict["file_name"],
        )
        
        print(f"s3_url: {s3_url}")

        if s3_url is not None:
            file_data = FileCreate(**new_file_dict)
            files_services.create_file_at_db(db, file_data)
            return JSONResponse(
                status_code=201,
                content={"message": "File uploaded and registered successfully"},
            )

        raise HTTPException(status_code=500, detail="Failed to upload file to S3.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



"""
{
    "file_name": "CV_Merino_Lautaro.pdf",
    "file_metadata": {
        "size": "66kb"
    },
    "file_type": "pdf",
    "folder_id": 1,
    "s3_url": "s3_url"
}
"""