from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas.schema import (
    UserCreate, UserUpdate, UserResponse
)
from services import users_services
"""(
    get_all_users,
    get_user_by_id,
    create_user,
    delete_user_by_id,
    update_user,
)
"""

router = APIRouter()

"""
    FALTA TERMINAR EL CRUD DE USERS
"""

@router.get("/get-users", response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    try:
        all_users = users_services.get_all_users(db)
        return all_users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obtaining users: {str(e)}")

@router.get("/get-user/{user_id}", response_model=UserResponse)
def get_all_users(user_id: int, db: Session = Depends(get_db)):
    try:
        user = users_services.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail=f"Not found user")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obtaining users: {str(e)}")
    
@router.delete("/delete-user/{user_id}")
def delete_user_by_id(user_id: int, db: Session = Depends(get_db)):
    try:
        users_services.delete_user_by_id(db, user_id)
        return JSONResponse(status_code=204)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting users: {str(e)}")
 
@router.post("/create-user", response_model=UserResponse)
def create_user(new_user: UserCreate, db: Session = Depends(get_db)):
    #try:
        new_user_id = users_services.create_user(db, new_user)
        user = users_services.get_user_by_id(db, new_user_id)
        return JSONResponse(
            status_code=201,
            content={
                "message": "User created successfully",
                "user": user
            }
        )
    #except Exception as e:
        #raise HTTPException(status_code=500, detail=f"Error creating users: {str(e)}")
    
@router.patch("/update-user/{user_id}")
def create_user(user_id: int, update_user: UserUpdate, db: Session = Depends(get_db)):
    try:
        user = users_services.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        updated_user = users_services.update_user(db, user_id, update_user)
        return JSONResponse(
            status_code=200,
            content={
                "message": "User updated successfully",
                "user": updated_user
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating users: {str(e)}")
