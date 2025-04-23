import streamlit as st
from tools.session_managment import close_session


def show_sidebar():
    """ This function creates the sidebar for the application. """
    with st.sidebar:
        st.markdown("## Menú")
        st.button("Inicio")
        st.button("Archivos")
        st.button("Configuración")
        if st.button("Cerrar sesión", on_click=close_session, key="close_session"):
            st.rerun()

