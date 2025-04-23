import streamlit as st


def init_session():
    """
    DOCSTRING
    """
    if "authenticated_user" not in st.session_state:
        st.session_state.authenticated_user = False
        st.session_state.user_data = {}


def add_user_to_session(user_data: dict):
    """
    DOCSTRING
    """
    st.session_state.authenticated_user = True
    st.session_state.user_data = {
        "name": user_data["full_name"] if " " not in user_data["full_name"] else user_data["full_name"].strip(" ")[0],
        "username": user_data["username"],
        "role": user_data["role"]
    }


def close_session():
    """
    DOCSTRING
    """
    st.session_state.authenticated_user = False
    st.session_state.user_data = {}
    
def is_authenticated():
    """
    DOCSTRING
    """
    return st.session_state.get("authenticated_user", False)


def get_user_data():
    """
    DOCSTRING
    """
    return st.session_state.get("user_data", {})
