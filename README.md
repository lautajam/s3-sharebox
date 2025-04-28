# 🗂️ s3_shrabocx

**s3_shrabocx** es un sistema de gestión de archivos y carpetas basado en Amazon S3 e inspirado en Google Drive. Incluye control de acceso por roles, etiquetado, metadatos, interfaz web y backend modularizado en contenedores Docker.

## 🚀 Tecnologías utilizadas

- **Backend:** Python 3 (FastAPI)
- **Frontend:** Python 3 (Streamlit)
- **Base de datos:** PostgreSQL 15
- **Docker:** Docker & Docker Compose

## ☁️ Servicios externos
- **Almacenamiento de archivos:** Amazon S3

## 🐳 Cómo levantar el proyecto
### 1. Construir e iniciar los contenedores
``docker compose up --build``

Esto levanta tres servicios:

- s3-db: Base de datos PostgreSQL
- s3-app: Backend con FastAPI
- s3-ui: Frontend con Streamlit

💡 Asegurate de tener Docker y Docker Compose instalados.

## 2. Acceder a la app
- 📂 Frontend (Streamlit): http://localhost:8501
- ⚙️ Backend (FastAPI docs): http://localhost:8000/docs
