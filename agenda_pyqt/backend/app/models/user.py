from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from ..db.base import Base

def get_utc_now():
    """Función helper para obtener el tiempo UTC actual"""
    return datetime.now(timezone.utc)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    email = Column(String(64), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(String(20), default="user")
    comision_porcentaje = Column(Float, default=0.0)
    fecha_creacion = Column(DateTime(timezone=True), default=get_utc_now)
    ultima_modificacion = Column(DateTime(timezone=True), default=get_utc_now, onupdate=get_utc_now)

    # Relaciones
    clientes_creados = relationship("Cliente", back_populates="creado_por_usuario", 
                                  foreign_keys="Cliente.creado_por_id")
    clientes_modificados = relationship("Cliente", back_populates="modificado_por_usuario",
                                      foreign_keys="Cliente.modificado_por_id")
