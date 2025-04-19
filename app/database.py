from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de la base de datos
DATABASE_URL = "postgresql://admin:1234@localhost:5432/gestor_s3"

# Crea el motor (engine) de la base de datos
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Crea la clase Base desde la que heredarán todos los modelos
Base = declarative_base()

# Crea la sesión para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)