import streamlit as st
from tools.login import hash_password

def login_page():
    st.title("S3 Sharebox")

    tab_login, tab_register = st.tabs(["Login", "Register"])

    with tab_login:
        with st.form(key='login_form'):
            user = st.text_input("User", type="default")
            password = st.text_input("Password", type="password")
            password_hashed = hash_password(password)
            submit_button = st.form_submit_button(label='Login')

            if submit_button:
                st.success("Login successful!")
    
    with tab_register:
        with st.form(key='register_form'):
            name = st.text_input("Name", type="default")
            user = st.text_input("User", type="default")
            email = st.text_input("Email", type="default")
            password = st.text_input("Password", type="password")
            password_hashed = hash_password(password)
            submit_button = st.form_submit_button(label='Register')

            if submit_button:
                st.success("Registration successful!")

def main():
    st.set_page_config(page_title="S3 Sharebox", page_icon=":cloud:", layout="centered")
    login_page()

if __name__ == "__main__":
    main()
