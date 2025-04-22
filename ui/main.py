import streamlit as st
from tools.login import hash_password, verify_user


def login_page():
    st.title("S3 Sharebox")

    tab_login, tab_register = st.tabs(["Login", "Register"])

    with tab_login:
        with st.form(key='login_form'):
            username = st.text_input("Username", type="default")
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button(label='Login')

            if submit_button:  
                if username == "" or password == "":
                    st.warning("Complete los campos, por favor", icon="⚠️")
                    st.stop()
                
                if verify_user(password, username) == -1:
                    st.error('Error al verificar usuario, recargue y vuelva a intentarlo', icon="❌")
                elif verify_user(password, username) == 0:
                    st.warning("Usuario no encontrado, compruebe credenciales", icon="⚠️")
                else:
                    st.success("Login successful!")
    
    with tab_register:
        with st.form(key='register_form'):
            name = st.text_input("Name", type="default")
            user = st.text_input("User", type="default")
            email = st.text_input("Email", type="default")
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button(label='Register')

            if submit_button:
                st.success("Registration successful!")

def main():
    st.set_page_config(page_title="S3 Sharebox", page_icon=":cloud:", layout="centered")
    login_page()

if __name__ == "__main__":
    main()
