from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from ..db.base import Base

class Corredor(Base):
    __tablename__ = "corredores"

    numero = Column(Integer, primary_key=True)  # Número de corredor
    nombre = Column(String(40), nullable=False)  # Nombre del corredor
    telefono = Column(String(20))  # Teléfono de contacto
    mail = Column(String(40), nullable=False)  # Correo electrónico
    observaciones = Column(Text)  # Observaciones adicionales

    # Relaciones
    clientes = relationship("Cliente", back_populates="corredor_rel")  # Relación con los clientes
    movimientos = relationship("MovimientoVigencia", back_populates="corredor_rel")
