import bcrypt

def hash_password(password: str, cost: int = 12) -> str:
    """Hashes a password using bcrypt with an optional cost factor.
    
    Args:
        password (str): The password to hash.
        cost (int, optional): The cost factor for bcrypt. Default is 12.
        
    Returns:
        str: The hashed password.
    
    Raises:
        ValueError: If the password is empty.
    """
    if not password:
        raise ValueError("Password cannot be empty.")
    
    salt = bcrypt.gensalt(rounds=cost)
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password.decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against a hashed password.
    
    Args:
        plain_password (str): The plain password to verify.
        hashed_password (str): The hashed password to compare against.
    
    Returns:
        bool: True if the passwords match, False otherwise.
        
    Raises:
        ValueError: If the plain password or hashed password is empty.
    """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))