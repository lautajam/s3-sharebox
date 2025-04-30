import os
import json
import urllib.parse
from typing import List
from database import get_db
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from schemas.role_schema import RoleCreate, RoleUpdate, RoleResponse
from services import roles_service

load_dotenv()
s3_bucket_name = os.getenv("S3_BUCKET")

router = APIRouter()

"""
get_all_roles-----------

get_role_by_id-----------

get_role_by_name------------

create_role

delete_role_by_id

update_role
"""

@router.post("/get-roles", response_model=List[RoleResponse])
def get_all_roles(db: Session = Depends(get_db)):
    """Get all roles from the database.

    Args:
        db (Session): SQLAlchemy session object

    Returns:
        List[Role]: List of Role objects

    Raises:
        HTTPException: If there is an error during the retrieval.
    """
    try:
        all_roles = roles_service.get_all_roles(db)
        if not all_roles:
            raise HTTPException(status_code=404, detail="No roles found")
        return all_roles
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obtaining roles. {str(e)}")

@router.post("/get-role-id", response_model=RoleResponse)
def get_role_by_id(role_id: int, db: Session = Depends(get_db)):
    """Get a role by ID from the database.
    
    Args:
        role_id (int): ID of the role to retrieve
        db (Session): SQLAlchemy session object
        
    Returns:
        Role: Role object if found, None otherwise
        
    Raises:
        HTTPException: If the role is not found or if there is an error during the retrieval.
    """
    try:
        role = roles_service.get_role_by_id(db, role_id)
        if not role:
            raise HTTPException(status_code=404, detail="Not found role")
        return role
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obtaining roles. {str(e)}")
    
@router.post("/get-role-name", response_model=RoleResponse)
def get_role_by_name(role_name: str, db: Session = Depends(get_db)):
    """Get a role by name from the database.
    
    Args:
        role_name (str): Name of the role to retrieve
        db (Session): SQLAlchemy session object
        
    Returns:
        Role: Role object if found, None otherwise
        
    Raises:
        HTTPException: If the role is not found or if there is an error during the retrieval.
    """
    try:
        role = roles_service.get_role_by_name(db, role_name)
        if not role:
            raise HTTPException(status_code=404, detail="Not found role")
        return role
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obtaining roles. {str(e)}")