import bcrypt
from api.endpoints import USER_ENDPOINTS
import requests
import os


def verify_user(username: str, password: str):
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

        print(f"Error: {e}")
        return -1
