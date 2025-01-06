from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from ..db.base import Base

class Corredor(Base):
    __tablename__ = "corredores"

    # Identificación
    numero = Column(Integer, primary_key=True)  # Número de corredor
    nombres = Column(String(30))  # Nombres del corredor
    apellidos = Column(String(30), nullable=False)  # Apellidos del corredor
    documento = Column(String(20), nullable=False, unique=True)  # Número de documento

    # Datos de contacto
    direccion = Column(String(70), nullable=False)  # Dirección del corredor
    localidad = Column(String(15), nullable=False)  # Localidad de residencia
    telefonos = Column(String(20))  # Teléfono fijo
    movil = Column(String(20))  # Teléfono móvil
    mail = Column(String(40), nullable=False, unique=True)  # Correo electrónico

    # Datos adicionales
    observaciones = Column(Text)  # Observaciones adicionales

    # Relaciones
    clientes = relationship("Cliente", back_populates="corredor_rel")  # Relación con los clientes
    movimientos = relationship("MovimientoVigencia", back_populates="corredor_rel")
