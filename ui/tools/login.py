from api.endpoints import USER_ENDPOINTS
from tools.constants import DEFAULT_ROLE
import requests

def verify_user(username: str, password: str):
    """Verify if the user exists in the database and if the password is correct.

    Args:
        username (str): The username of the user.
        password (str): The password of the user.

    Returns:
        int: 1 if the user exists and the password is correct,
             0 if the user does not exist or the password is incorrect,
             -1 if an error occurs.
    """
    try:
        response_user_password = requests.get(
            USER_ENDPOINTS["get_user_by_password_username"](username, password)
        )

        if not response_user_password:
            return 0

        response_user_password_json = response_user_password.json()
        if response_user_password_json["username"] == username:
            return 1

        return 0
    except Exception as e:
        return -1


def create_user(full_name: str, username: str, password: str):
    """Create a new user in the database.

    Args:
        full_name (str): The full name of the user.
        username (str): The username of the user.
        password (str): The password of the user.

    Returns:
        int: 1 if the user was created successfully,
             0 if the user already exists,
             -1 if an error occurs.
    """

    new_user_dict = {
        "full_name": full_name,
        "username": username,
        "password": password,
        "role_id": DEFAULT_ROLE,
    }

    try:
        response_create_user = requests.post(
            USER_ENDPOINTS["create_user"], json=new_user_dict
        )

        if response_create_user.status_code == 201:
            return 1
        elif response_create_user.status_code == 409:
            return 0

        return -1
    except Exception as e:
        return -1

def get_user_to_add_session(username: str) -> dict | None:
    """Get user data by username.
    
    Args:
        username (str): The username of the user.
        
    Returns:
        dict: A dictionary containing the user's full name, username, and role.
              Returns None if the user is not found or an error occurs.
              
    Raises:
        Exception: If an error occurs during the request.
    """
    try:
        response = requests.get(USER_ENDPOINTS["get_user_by_username"](username))

        if response.status_code != 200:
            return None

        user_data_raw = response.json()

        if user_data_raw.get("username") != username:
            return None

        return {
            "full_name": user_data_raw["full_name"],
            "username": user_data_raw["username"],
            "role": user_data_raw["role_id"]
        }

    except:
        return {"error": -1}