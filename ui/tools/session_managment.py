import streamlit as st


def init_session():
    """ This function initializes the session state for the Streamlit app.
    It checks if the session state has the key 'authenticated_user', and if not,
    """
    if "authenticated_user" not in st.session_state:
        st.session_state.authenticated_user = False
        st.session_state.user_data = {}


def add_user_to_session(user_data: dict):
    """ This function adds user data to the session state.
    It sets the 'authenticated_user' key to True and stores the user's name,
    username, and role in the 'user_data' key of the session state.
    
    Args:
        user_data (dict): A dictionary containing user data. It should contain
                          the keys 'full_name', 'username', and 'role'.
    """
    st.session_state.authenticated_user = True
    st.session_state.user_data = {
        "name": user_data["full_name"] if " " not in user_data["full_name"] else user_data["full_name"].strip(" ")[0],
        "username": user_data["username"],
        "role": user_data["role"]
    }


def close_session():
    """ This function closes the session.
    """
    st.session_state.authenticated_user = False
    st.session_state.user_data = {}
    
def is_authenticated():
    """ This function checks if the user is authenticated.
    """
    return st.session_state.get("authenticated_user", False)


def get_user_data():
    """ This function retrieves the user data from the session state.
    """
    return st.session_state.get("user_data", {})


def files_session():
    """ This function initializes the session state for files.
    It checks if the session state has the key 'files', and if not,
    it initializes it as an empty list.
    """
    if "files" not in st.session_state:
        st.session_state.files = None