from sqlalchemy.orm import Session
from models.model import User
from schemas.schema import UserCreate, UserUpdate

def get_all_users(db : Session):
    """ Get all users from the database.
    
    Args:
        db (Session): SQLAlchemy session object

    Returns:
        List[User]: a list of User objects
    """
    
    return db.query(User).all()

def get_user_by_id(db: Session, user_id: int):
    """ Get a user by ID from the database.
   
    Args:
        db (Session): SQLAlchemy session object
        user_id (int): ID of the user to retrieve
        
    Returns:
        User: User object if found, None otherwise
    """
    
    return db.query(User).filter(User.user_id == user_id).first()

def create_user(db: Session, user_data: UserCreate):
    """ Create a new user in the database.
    
    Args:
        db (Session): SQLAlchemy session object
        user_data (UserCreate): User data to create a new user
        
    Returns:
        User: Created User object
    """
    
    new_user = User(**user_data.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def delete_user_by_id(db: Session, user_id: int):
    """ Delete a user by ID from the database.
    
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
    """ Update a user in the database.
    
    Args:
        db (Session): SQLAlchemy session object
        user_id (int): ID of the user to update
        user_update (UserUpdate): User data to update
        
    Returns:
        User: Updated User object if found, None otherwise
    """
    
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        return None

    for field, value in user_update.dict(exclude_unset=True).items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user