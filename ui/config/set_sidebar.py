import streamlit as st


def show_sidebar():
    with st.sidebar:
        st.markdown("## Menú")
        st.button("Inicio")
        st.button("Archivos")
        st.button(
            "Salir",
        )
