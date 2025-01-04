from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime, timezone
from ..db.base import Base

def get_utc_now():
    """Función helper para obtener el tiempo UTC actual"""
    return datetime.now(timezone.utc)

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)  # UUID como clave primaria
    nombres = Column(String(30), nullable=False)  # Nombre del cliente
    apellidos = Column(String(30), nullable=False)  # Apellido del cliente
    tipo_documento = Column(String(4), nullable=False)  # Tipo de documento (DNI, CI, RUT, CUIT)
    numero_documento = Column(String(20), nullable=False, unique=True, index=True)  # Número de documento
    fecha_nacimiento = Column(Date, nullable=False)  # Fecha de nacimiento
    direccion = Column(String(70), nullable=False)  # Dirección completa
    localidad = Column(String(15))  # Ciudad o localidad
    telefonos = Column(String(20), nullable=False)  # Teléfono fijo
    movil = Column(String(20), nullable=False)  # Teléfono móvil/celular
    mail = Column(String(50), nullable=False, unique=True, index=True)  # Correo electrónico
    corredor = Column(Integer, ForeignKey("corredores.numero"))  # ID del corredor asignado
    observaciones = Column(Text)  # Observaciones adicionales
    creado_por_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Usuario que creó el registro
    modificado_por_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Usuario que modificó por última vez
    fecha_creacion = Column(DateTime(timezone=True), default=get_utc_now)  # Fecha y hora de creación
    fecha_modificacion = Column(DateTime(timezone=True), default=get_utc_now, onupdate=get_utc_now)  # Fecha y hora de última modificación

    # Relaciones
    creado_por_usuario = relationship("User", foreign_keys=[creado_por_id], back_populates="clientes_creados")
    modificado_por_usuario = relationship("User", foreign_keys=[modificado_por_id], back_populates="clientes_modificados")
    movimientos_vigencias = relationship("MovimientoVigencia", back_populates="cliente_rel", cascade="all, delete-orphan")
    corredor_rel = relationship("Corredor", back_populates="clientes")  # Relación con el corredor
