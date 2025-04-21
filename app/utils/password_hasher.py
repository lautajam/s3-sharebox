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