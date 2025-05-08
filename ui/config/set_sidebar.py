import streamlit as st
from tools.session_managment import close_session
from tools.file_managment import upload_file
from time import sleep

def show_sidebar():
    """ This function creates the sidebar for the application. """
    if "show_upload_modal" not in st.session_state:
        st.session_state.show_upload_modal = False
        
    with st.sidebar:
        st.markdown("## Menú")
        #st.button("Gestión de Archivos")
        if st.button("Subir Archivo", key="upload_file"):
            st.session_state.show_upload_modal = not st.session_state.show_upload_modal

        if st.session_state.show_upload_modal:
            with st.container():
                st.markdown("---")
                uploaded_file = st.file_uploader("Selecciona un archivo")

                col1, col2 = st.columns(2)

                with col1:
                    if st.button("✅"):
                        if uploaded_file:
                            # Aquí podrías guardar el archivo o hacer otra acción
                            is_upload = upload_file(uploaded_file, user_id=st.session_state.user_data["user_id"])
                            if is_upload == 1:
                                st.error("Error al subir el archivo.")
                            else:
                                st.success("Subido")
                                st.session_state.show_upload_modal = False
                        else:
                            st.warning("Primero selecciona un archivo.")

                with col2:
                    if st.button("❌"):
                        st.session_state.show_upload_modal = False
                st.markdown("---")
        #st.button("Configuración")
        if st.button("Cerrar sesión", on_click=close_session, key="close_session"):
            st.rerun()

