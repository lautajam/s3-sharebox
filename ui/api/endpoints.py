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
    "get_files_by_filter": lambda select_filter, select_order: f"{BASE_URL}/files/get-files-filter/{select_filter}/{select_order}",
    "get_file_by_id": lambda file_id: f"{BASE_URL}/files/get-file-id/{file_id}",
    "get_file_by_name": lambda file_name: f"{BASE_URL}/files/get-file-name/{file_name}",
    "get_file_by_user_id": lambda user_id: f"{BASE_URL}/files/get-file-user-id/{user_id}",
    "upload_register_file": f"{BASE_URL}/files/upload-register-file/",
}
