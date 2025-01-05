"""
Modelo para la entidad Usuario.
"""
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from sqlalchemy.orm import relationship
from ..db.base_class import Base
from datetime import datetime, timezone

def get_utc_now():
    """Función helper para obtener el tiempo UTC actual"""
    return datetime.now(timezone.utc)

class Usuario(Base):
    """Modelo para la tabla usuarios."""
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(64), nullable=False)
    apellido = Column(String(64), nullable=False)
    email = Column(String(64), nullable=False, unique=True)
    username = Column(String(64), unique=True, index=True, nullable=False)
    hashed_password = Column(String(128), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    role = Column(String(20), default="user")
    comision_porcentaje = Column(Float, default=0.0)
    fecha_creacion = Column(DateTime(timezone=True), default=get_utc_now)
    fecha_modificacion = Column(DateTime(timezone=True), default=get_utc_now, onupdate=get_utc_now)

    # Relaciones
    clientes_creados = relationship(
        "Cliente", 
        back_populates="creado_por_usuario", 
        foreign_keys="Cliente.creado_por_id"
    )
    clientes_modificados = relationship(
        "Cliente", 
        back_populates="modificado_por_usuario",
        foreign_keys="Cliente.modificado_por_id"
    )
