import bcrypt
from api.endpoints import USER_ENDPOINTS
import requests
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


def verify_user(password: str, username: str):
    try:
        list_response_users_password = requests.get(USER_ENDPOINTS['get_user_by_password'](password))
        
        if not list_response_users_password:
            return 0
        
        list_response_users_password_json = list_response_users_password.json()

        for user in list_response_users_password_json:
            if user['username'] == username:
                return 1
        
        return 0
    except Exception as e:
        
        print(f"Error: {e}")
        return -1
    