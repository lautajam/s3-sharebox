
from api.endpoints import FILES_ENDPOINTS, USER_ENDPOINTS
import requests

def get_all_files():
    """ This function retrieves all files from the API.
    It sends a GET request to the API endpoint and returns the response.
    """
    try:
        response = requests.get(FILES_ENDPOINTS["get_files"])
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching files: {e}")
        return None
    
def get_user_by_id(user_id):
    """ This function retrieves a user by their ID from the API.
    It sends a GET request to the API endpoint and returns the response.
    """
    try:
        response = requests.get(USER_ENDPOINTS["get_user_by_id"](user_id))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching user by ID: {e}")
        return None
    
def get_files_by_filter(filter, order):
    """ This function retrieves files by filter and order from the API.
    It sends a GET request to the API endpoint and returns the response.
    """
    try:
        response = requests.get(FILES_ENDPOINTS["get_files_by_filter"], params={"select_filter": filter, "select_order": order})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return None
    
def upload_file(file, user_id):
    """
    This function uploads a file to the API.
    It sends a POST request to the API endpoint with the file data and metadata.
    """
    try:
        files = {
            'uploaded_file': file
        }
        data = {
            'folder_id': 3,
            'owner_id': user_id
        }
        response = requests.post(FILES_ENDPOINTS["upload_register_file"], files=files, data=data)
        response.raise_for_status()
        return 0
    except requests.exceptions.RequestException as e:
        return 1