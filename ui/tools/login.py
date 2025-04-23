from api.endpoints import USER_ENDPOINTS
import requests

DEFAULT_ROLE = 2


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
