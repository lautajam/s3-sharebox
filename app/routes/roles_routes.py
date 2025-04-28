import os
import json
import urllib.parse
from typing import List
from database import get_db
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form

load_dotenv()
s3_bucket_name = os.getenv("S3_BUCKET")

router = APIRouter()


@router.post("/home-role")
def home_try():
    return JSONResponse(
        status_code=200,
        content={
            "message": "Welcome to the home route for roles!"
        },
    )