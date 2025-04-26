from sqlalchemy.orm import Session
from models.model import User
from schemas.user_schema import UserCreate, UserUpdate
from utils.password_hasher import hash_password, verify_password

def get_all_users(db: Session):
    """Get all users from the database.

    Args:
        db (Session): SQLAlchemy session object

    Returns:
        List[User]: a list of User objects
    """

    return db.query(User).all()


def get_user_by_id(db: Session, user_id: int):
    """Get a user by ID from the database.

    Args:
        db (Session): SQLAlchemy session object
        user_id (int): ID of the user to retrieve

    Returns:
        User: User object if found, None otherwise
    """

    return db.query(User).filter(User.user_id == user_id).first()


def get_user_by_username(db: Session, username: str):
    """Get a user by username from the database.

    Args:
        db (Session): SQLAlchemy session object
        username (str): Username of the user to retrieve

    Returns:
        User: User object if found, None otherwise
    """

    return db.query(User).filter(User.username == username).first()


def get_user_by_password(db: Session, password: str):
    """Get a user by password from the database.

    Args:
        db (Session): SQLAlchemy session object
        password (str): Password of the user to retrieve

    Returns:
        User: User object if found, None otherwise
    """
    
    password_hashed = hash_password(password)

    return db.query(User).filter(User.password == password_hashed).all()


def get_user_by_password_username(db: Session,  username:str, password: str):
    """Get a user by password and username from the database.
    
    Args:
        db (Session): SQLAlchemy session object
        password (str): Password of the user to retrieve
        username (str): Username of the user to retrieve
        
    Returns:
        User: User object if found, None otherwise
    """

    user = db.query(User).filter(User.username == username).first()
    
    if user and verify_password(password, user.password):
        return user
    
    return None


def create_user(db: Session, user_data: UserCreate):
    """Create a new user in the database.

    Args:
        db (Session): SQLAlchemy session object
        user_data (UserCreate): User data to create a new user

    Returns:
        User: Created User object
    """

    new_user = User(**user_data.dict())
    new_user.password = hash_password(user_data.password)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def delete_user_by_id(db: Session, user_id: int):
    """Delete a user by ID from the database.

    Args:
        db (Session): SQLAlchemy session object
        user_id (int): ID of the user to delete

    Returns:
        User: Deleted User object if found, None otherwise
    """

    delete_user = get_user_by_id(db, user_id)
    if delete_user:
        db.delete(delete_user)
        db.commit()
    return delete_user


def update_user(db: Session, user_id: int, user_update: UserUpdate):
    """Update a user in the database.

    Args:
        db (Session): SQLAlchemy session object
        user_id (int): ID of the user to update
        user_update (UserUpdate): User data to update

    Returns:
        User: Updated User object if found, None otherwise
    """

    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        return False

    for field, value in user_update.dict(exclude_unset=True).items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return True
