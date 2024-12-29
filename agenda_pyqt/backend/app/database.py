from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Generator
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde la raíz del proyecto
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env'))

# Obtener DATABASE_URL directamente del archivo .env
DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    # Si no se encuentra DATABASE_URL, construirlo a partir de las variables individuales
    POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')
    POSTGRES_DB = os.getenv('POSTGRES_DB', 'seguros')
    POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'postgres')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
    
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Configuración del engine con opciones de pool
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Verifica la conexión antes de usarla
    pool_size=5,  # Tamaño del pool de conexiones
    max_overflow=10,  # Máximo de conexiones adicionales
    pool_timeout=30  # Tiempo máximo de espera para una conexión
)

# Configuración de la sesión
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False  # Mejora el rendimiento evitando recargas innecesarias
)

Base = declarative_base()

def get_db() -> Generator:
    """
    Genera una nueva sesión de base de datos.
    
    Yields:
        Session: Sesión de SQLAlchemy para interactuar con la base de datos.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()