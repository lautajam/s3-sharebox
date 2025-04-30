import os

BASE_URL = os.getenv("API_BASE_URL")

USER_ENDPOINTS = {
    "get_users": f"{BASE_URL}/users/get-users",
    "get_user_by_id": lambda user_id: f"{BASE_URL}/users/get-user-id/{user_id}",
    "get_user_by_username": lambda username: f"{BASE_URL}/users/get-user-username/{username}",
    "get_user_by_password": lambda password: f"{BASE_URL}/users/get-user-password/{password}",
    "get_user_by_password_username": lambda username, password: f"{BASE_URL}/users/get-user-password-username/{username}/{password}",
    "delete_user": lambda user_id: f"{BASE_URL}/users/delete-user/{user_id}",
    "create_user": f"{BASE_URL}/users/create-user",
    "update_user": lambda user_id: f"{BASE_URL}/users/update-user/{user_id}",
}

FILES_ENDPOINTS = {
    "get_files": f"{BASE_URL}/files/get-files",
    "get_file_by_id": lambda file_id: f"{BASE_URL}/files/get-file-id/{file_id}",
    "get_file_by_name": lambda file_name: f"{BASE_URL}/files/get-file-name/{file_name}",
    "get_file_by_user_id": lambda user_id: f"{BASE_URL}/files/get-file-user-id/{user_id}",
    "create_file": f"{BASE_URL}/files/create-file",
    "update_file": lambda file_id: f"{BASE_URL}/files/update-file/{file_id}",
    "delete_file": lambda file_id: f"{BASE_URL}/files/delete-file/{file_id}",
}
