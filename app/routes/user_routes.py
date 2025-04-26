from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas.user_schema import UserCreate, UserUpdate, UserResponse
from services import users_services

router = APIRouter()


@router.get("/get-users", response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    """Get all users from the database.

    Args:
        db (Session): SQLAlchemy session object

    Returns:
        List[User]: List of User objects

    Raises:
        HTTPException: If there is an error during the retrieval.
    """
    try:
        all_users = users_services.get_all_users(db)
        return all_users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obtaining users. {str(e)}")


@router.get("/get-user-id/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """Get a user by ID from the database.

    Args:
        user_id (int): ID of the user to retrieve
        db (Session): SQLAlchemy session object

    Returns:
        User: User object if found, None otherwise

    Raises:
        HTTPException: If the user is not found or if there is an error during the retrieval.
    """
    try:
        user = users_services.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail=f"Not found user")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obtaining users. {str(e)}")


@router.get("/get-user-username/{username}", response_model=UserResponse)
def get_user_by_username(username: str, db: Session = Depends(get_db)):
    """Get a user by username from the database.

    Args:
        username (str): Username of the user to retrieve
        db (Session): SQLAlchemy session object

    Returns:
        User: User object if found, None otherwise

    Raises:
        HTTPException: If the user is not found or if there is an error during the retrieval.
    """
    try:
        user = users_services.get_user_by_username(db, username)
        if not user:
            raise HTTPException(status_code=404, detail=f"Not found user")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obtaining users. {str(e)}")


@router.get("/get-user-password/{password}", response_model=List[UserResponse])
def get_user_by_password(password: str, db: Session = Depends(get_db)):
    """Get a user by password from the database.

    Args:
        password (str): Password of the user to retrieve
        db (Session): SQLAlchemy session object

    Returns:
        User: User object if found, None otherwise

    Raises:
        HTTPException: If the user is not found or if there is an error during the retrieval.
    """
    try:
        users = users_services.get_user_by_password(db, password)
        if not users:
            raise HTTPException(status_code=404, detail=f"Not found user")
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obtaining users. {str(e)}")


@router.get(
    "/get-user-password-username/{username}/{password}", response_model=UserResponse
)
def get_user_by_password_username(
    username: str, password: str, db: Session = Depends(get_db)
):
    """Get a user by password and username from the database.

    Args:
        password (str): Password of the user to retrieve
        username (str): Username of the user to retrieve
        db (Session): SQLAlchemy session object

    Returns:
        User: User object if found, None otherwise
    Raises:
        HTTPException: If the user is not found or if there is an error during the retrieval.
    """

    try:
        user = users_services.get_user_by_password_username(db, username, password)
        if not user:
            raise HTTPException(status_code=404, detail=f"Not found user")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obtaining users. {str(e)}")


@router.delete("/delete-user/{user_id}")
def delete_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """Delete a user by ID from the database.

    Args:
        user_id (int): ID of the user to delete
        db (Session): SQLAlchemy session object

    Returns:
        JSONResponse: Response indicating the result of the deletion

    Raises:
        HTTPException: If the user is not found or if there is an error during the deletion.
    """
    try:
        users_services.delete_user_by_id(db, user_id)
        return JSONResponse(
            status_code=200,
            content={"message": f"User #{user_id} deleted successfully"},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting user. {str(e)}")


@router.post("/create-user", response_model=UserResponse)
def create_user(new_user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user in the database.

    Args:
        new_user (UserCreate): User data to create a new user
        db (Session): SQLAlchemy session object

    Returns:
        User: Created User object

    Raises:
        HTTPException: If there is an error during the creation.
    """
    try:
        if users_services.get_user_by_username(db, new_user.username):
            return JSONResponse(
                status_code=409, content={"message": "Username already in use"}
            )
        users_services.create_user(db, new_user)
        return JSONResponse(
            status_code=201, content={"message": "User created successfully"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating users: {str(e)}")


@router.patch("/update-user/{user_id}", response_model=UserResponse)
def update_user(user_id: int, update_user: UserUpdate, db: Session = Depends(get_db)):
    """Update a user by ID in the database.

    Args:
        user_id (int): ID of the user to update
        update_user (UserUpdate): User data to update
        db (Session): SQLAlchemy session object

    Returns:
        User: Updated User object if found, None otherwise

    Raises:
        HTTPException: If the user is not found or if there is an error during the update.
    """
    try:
        user = users_services.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        exist_user = users_services.update_user(db, user_id, update_user)

        if exist_user:
            updated_user = users_services.get_user_by_id(db, user_id)
        else:
            raise HTTPException(status_code=404, detail="User not found")

        return updated_user

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating users. {str(e)}")
