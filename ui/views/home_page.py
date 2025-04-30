import streamlit as st
from tools.constants import ADMIN_ROLE
from time import sleep
from tools.file_managment import get_all_files, get_user_by_id


def home_page():
    st.markdown("## 📁 Gestor de Archivos")
    st.markdown("---")

    with st.container():
        col1, col2, col3 = st.columns([3, 3, 1])
        flag = False

        with col1:
            select_filter = st.selectbox(
                "🔍 Filtrar por",
                ["---", "Nombre", "Fecha", "Tipo", "Tamaño", "Usuario"],
                help="Selecciona un criterio para filtrar los archivos",
            )

        with col2:
            select_order = st.selectbox(
                "↕️ Ordenar por",
                ["---", "Ascendente", "Descendente"],
                help="Selecciona el orden de visualización",
            )

        with col3:
            # Espaciado para alinear el botón con los selectbox
            st.write("")  # línea vacía para separación
            st.write("")  # otra línea vacía
            flag = st.button("Aplicar", use_container_width=True)

        if flag:
            if select_filter == "---" or select_order == "---":
                st.warning("Por favor, selecciona un filtro y un orden válidos.")
            else:
                st.success(f"Aplicando filtro: {select_filter} y orden: {select_order}")
                sleep(2)
                st.rerun()
                
    st.markdown("---")

    with st.container():

        files = get_all_files()

        if files:
            for file in files:
                with st.expander(f"📄 {file['file_name']}"):
                    col1, col2, col3 = st.columns([2, 2, 1])

                    with col1:
                        st.markdown(f"**📁 Tipo:** {file.get('file_type', 'N/A')}")
                        st.markdown(f"**🗓️ Fecha:** {file.get('uploaded_at', 'N/A')}")

                    with col2:
                        user_info = (
                            get_user_by_id(file.get("owner_id"))
                            if file.get("owner_id")
                            else None
                        )
                        username = (
                            user_info.get("username") if user_info else "No disponible"
                        )
                        st.markdown(f"**👤 Usuario:** {username}")
                        st.markdown(
                            f"**📏 Tamaño:** {file.get('file_metadata', {}).get('size', 'N/A')}"
                        )

                    col1, col2 = st.columns([2, 2])
                    with col1:
                        st.button(
                            "⬇️ Descargar", key=file["file_id"], help="Descargar archivo"
                        )
                    with col2:
                        st.button(
                            "🗑️ Eliminar",
                            key=f"delete_{file['file_id']}",
                            help="Eliminar archivo",
                        )

    st.markdown("---")
