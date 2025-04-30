
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