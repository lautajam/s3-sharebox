import streamlit as st
from tools.login import verify_user, create_user, get_user_to_add_session
from tools.session_managment import init_session, add_user_to_session, is_authenticated
from tools.constants import DEFAULT_ROLE
import time


def login_page():
    st.title("S3 Sharebox")

    tab_login, tab_register = st.tabs(["Login", "Register"])

    with tab_login:
        with st.form(key="login_form"):
            username = st.text_input("Username", type="default")
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button(label="Login")

            if submit_button:
                if username == "" or password == "":
                    st.warning("Complete los campos, por favor", icon="⚠️")
                    st.stop()

                verify_user_bool = verify_user(username, password)

                if verify_user_bool == -1:
                    st.error(
                        "Error al verificar usuario, recargue y vuelva a intentarlo",
                        icon="❌",
                    )
                elif verify_user_bool == 0:
                    st.warning(
                        "Usuario no encontrado, compruebe credenciales", icon="⚠️"
                    )
                else:
                    st.success("Login successful!")
                    user_data = get_user_to_add_session(username)

                    if user_data is None or "error" in user_data:
                        st.error("Error al obtener datos del usuario", icon="❌")
                        st.stop()

                    add_user_to_session(user_data)

                    time.sleep(2)

                    st.switch_page("pages/home.py")

    with tab_register:
        with st.form(key="register_form"):
            full_name = st.text_input("Name", type="default")
            username = st.text_input("User", type="default")
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button(label="Register")

            if submit_button:

                verify_user_bool = create_user(full_name, username, password)

                if verify_user_bool == -1:
                    st.error(
                        "Error al crear usuario, recargue y vuelva a intentarlo",
                        icon="❌",
                    )
                elif verify_user_bool == 0:
                    st.warning("Username ya en uso, elija otro", icon="⚠️")
                else:
                    st.success("Registration successful!")

                    user_data = {
                        "full_name": full_name,
                        "username": username,
                        "role": DEFAULT_ROLE,
                    }

                    add_user_to_session(user_data)

                    time.sleep(2)

                    st.switch_page("pages/home.py")


def main():
    st.set_page_config(page_title="S3 Sharebox", page_icon=":cloud:", layout="centered")
    init_session()
    if is_authenticated():
        st.switch_page("pages/home.py")
    login_page()


if __name__ == "__main__":
    main()
