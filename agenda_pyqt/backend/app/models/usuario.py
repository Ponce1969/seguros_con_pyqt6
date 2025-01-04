"""
Modelos relacionados con la entidad Usuario.
"""
from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timezone

def get_utc_now():
    """Función helper para obtener el tiempo UTC actual"""
    return datetime.now(timezone.utc)

class Usuario(Base):
    """Modelo para la tabla usuarios."""
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    fecha_creacion = Column(DateTime(timezone=True), default=get_utc_now)
    fecha_modificacion = Column(DateTime(timezone=True), default=get_utc_now, onupdate=get_utc_now)
