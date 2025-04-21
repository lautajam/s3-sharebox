import bcrypt
import os

def hash_password(password: str) -> str:
    """ Hashes a password using bcrypt.
    
    Args:
        password (str): The password to hash.
        
    Returns:
        str: The hashed password.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    
    return hashed_password.decode('utf-8')