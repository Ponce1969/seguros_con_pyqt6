"""
Modelos relacionados con la entidad Cliente.
"""
from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey, DateTime, Sequence, BigInteger
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime, timezone
from ..db.base import Base

def get_utc_now():
    """Función helper para obtener el tiempo UTC actual"""
    return datetime.now(timezone.utc)

class Cliente(Base):
    """Modelo para la tabla clientes con numeración segura."""
    __tablename__ = "clientes"

    # Secuencia para numero_cliente
    cliente_seq = Sequence('cliente_numero_seq')

    # Campos de identificación
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    numero_cliente = Column(
        BigInteger,
        Sequence('cliente_numero_seq'),
        unique=True,
        nullable=False,
        index=True
    )

    # Datos personales
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    tipo_documento = Column(String(50), nullable=False)
    numero_documento = Column(String(50), nullable=False, unique=True, index=True)
    fecha_nacimiento = Column(Date, nullable=False)
    
    # Datos de contacto
    direccion = Column(String(200), nullable=False)
    localidad = Column(String(50))
    telefonos = Column(String(100), nullable=False)
    movil = Column(String(100), nullable=False)
    mail = Column(String(100), nullable=False, unique=True, index=True)
    
    # Datos del negocio
    corredor = Column(Integer, ForeignKey("corredores.numero"))
    observaciones = Column(Text)
    
    # Campos de auditoría
    creado_por_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    modificado_por_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    fecha_creacion = Column(DateTime(timezone=True), default=get_utc_now)
    fecha_modificacion = Column(DateTime(timezone=True), default=get_utc_now, onupdate=get_utc_now)

    # Relaciones
    creado_por_usuario = relationship("User", foreign_keys=[creado_por_id], back_populates="clientes_creados")
    modificado_por_usuario = relationship("User", foreign_keys=[modificado_por_id], back_populates="clientes_modificados")
    movimientos_vigencias = relationship("MovimientoVigencia", back_populates="cliente_rel", cascade="all, delete-orphan")
    corredor_rel = relationship("Corredor", back_populates="clientes")
