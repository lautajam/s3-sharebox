import os

BASE_URL = os.getenv("API_BASE_URL")

USER_ENDPOINTS = {
    "get_users": f"{BASE_URL}/get-users",
    "get_user_by_id": lambda user_id: f"{BASE_URL}/get-user-id/{user_id}",
    "get_user_by_username": lambda username: f"{BASE_URL}/get-user-username/{username}",
    "get_user_by_password": lambda password: f"{BASE_URL}/get-user-password/{password}",
    "delete_user": lambda user_id: f"{BASE_URL}/delete-user/{user_id}",
    "create_user": f"{BASE_URL}/create-user",
    "update_user": lambda user_id: f"{BASE_URL}/update-user/{user_id}",
}