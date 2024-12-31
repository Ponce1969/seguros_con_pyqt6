"""
Modelos relacionados con la entidad MovimientoVigencia.
"""
from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

from app.database import Base

class MovimientoVigencia(Base):
    """Modelo para la tabla movimientos_vigencias."""
    __tablename__ = "movimientos_vigencias"

    Id_movimiento = Column(Integer, primary_key=True, index=True)
    FechaMov = Column(Date)
    Corredor = Column(Integer)
    Cliente = Column(BigInteger, ForeignKey("clientes.numero_cliente"))  # Referencia al número de cliente
    Tipo_seguro = Column(Integer)
    Carpeta = Column(String(100))
    Poliza = Column(String(100), nullable=True)
    Endoso = Column(String(100), nullable=True)
    Vto_Desde = Column(Date)
    Vto_Hasta = Column(Date)
    Moneda = Column(String(10))
    Premio = Column(Float, nullable=True)
    Cuotas = Column(Integer, nullable=True)
    Observaciones = Column(String(500), nullable=True)

    # Relación con el cliente
    cliente = relationship("Cliente", back_populates="movimientos")
