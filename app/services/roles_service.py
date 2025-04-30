from sqlalchemy.orm import Session
from models.model import Role
from schemas.role_schema import RoleCreate, RoleUpdate, RoleResponse
from utils.password_hasher import hash_password, verify_password

def get_all_roles(db: Session):
    """Get all roles from the database.

    Args:
        db (Session): SQLAlchemy session object

    Returns:
        List[Role]: a list of Roles objects
    """

    return db.query(Role).all()


def get_role_by_id(db: Session, role_id: int):
    """Get a role by ID from the database.
    
    Args:
        db (Session): SQLAlchemy session object
        role_id (int): ID of the role to retrieve
        
    Returns:
        Role: Role object if found, None otherwise
    """
    return db.query(Role).filter(Role.role_id == role_id).first()


def get_role_by_name(db: Session, role_name: str):
    """ Get a role by name from the database.
    
    Args:
        db (Session): SQLAlchemy session object
        role_name (str): Name of the role to retrieve
        
    Returns:
        Role: Role object if found, None otherwise
    """

    return db.query(Role).filter(Role.role_name == role_name).first()


def create_role(db: Session, role_data: RoleCreate):
    """ Create a new role in the database.
    
    Args:
        db (Session): SQLAlchemy session object
        role_data (RoleCreate): Role data to create
        
    Returns:
        Role: Created Role object
    """

    new_role = Role(**role_data.dict())
    
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role


def delete_role_by_id(db: Session, role_id: int):
    """Delete a role by ID from the database.
    
    Args:
        db (Session): SQLAlchemy session object
        role_id (int): ID of the role to delete
        
    Returns:
        Role: Deleted Role object if found, None otherwise
    """

    delete_role = get_role_by_id(db, role_id)
    if delete_role:
        db.delete(delete_role)
        db.commit()
    return delete_role


def update_role(db: Session, role_id: int, role_update: RoleUpdate):
    """Update a role in the database.
    
    Args:
        db (Session): SQLAlchemy session object
        role_id (int): ID of the role to update
        role_update (RoleUpdate): Role data to update
        
    Returns:
        bool: True if update was successful, False otherwise
    """

    role = db.query(Role).filter(Role.role_id == role_id).first()
    if not role:
        return False

    for field, value in role_update.dict(exclude_unset=True).items():
        setattr(role, field, value)

    db.commit()
    db.refresh(role)
    return True
