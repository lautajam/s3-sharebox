import streamlit as st
from tools.session_managment import init_session, is_authenticated
from config.set_sidebar import show_sidebar
from views.login_page import login_page
from views.home_page import home_page


st.set_page_config(page_title="S3 Sharebox", page_icon=":cloud:", layout="centered")
init_session()


def main():
    if not is_authenticated():
        login_page()
    else:
        show_sidebar()
        home_page()


if __name__ == "__main__":
    main()
