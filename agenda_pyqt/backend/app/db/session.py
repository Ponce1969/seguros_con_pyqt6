from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator
from ..core.config import settings

# Configuración del engine con opciones de pool
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
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
