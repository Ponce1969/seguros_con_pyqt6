"""
Modelos relacionados con la entidad Cliente.
"""
from datetime import datetime
from sqlalchemy import Column, String, BigInteger, Integer, Date, DateTime, Text, Sequence
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from app.database import Base

class Cliente(Base):
    """Modelo para la tabla clientes con numeración segura."""
    __tablename__ = "clientes"

    # Secuencia para numero_cliente
    cliente_seq = Sequence('cliente_numero_seq')

    # Campos de identificación
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    numero_cliente = Column(
        BigInteger,
        Sequence('cliente_numero_seq'),
        unique=True,
        nullable=False,
        index=True
    )

    # Datos personales
    nombres = Column(String(100))
    apellidos = Column(String(100), nullable=False)
    tipo_documento = Column(String(50))
    documentos = Column(String(50), unique=True, index=True)
    fecha_nacimiento = Column(Date)
    
    # Datos de contacto
    direccion = Column(String(200), nullable=False)
    localidad = Column(String(50))
    telefonos = Column(String(100))
    movil = Column(String(100))
    mail = Column(String(100), unique=True, index=True)
    
    # Datos del negocio
    corredor = Column(Integer, index=True)
    observaciones = Column(Text)
    
    # Campos de auditoría
    creado_por_id = Column(Integer, nullable=False)
    modificado_por_id = Column(Integer, nullable=False)
    fecha_creacion = Column(DateTime, nullable=False, default=datetime.utcnow)
    fecha_modificacion = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    movimientos = relationship("MovimientoVigencia", back_populates="cliente", cascade="all, delete-orphan")
