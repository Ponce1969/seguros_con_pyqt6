"""
Modelos relacionados con la entidad MovimientoVigencia.
"""
from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from ..db.base import Base

class MovimientoVigencia(Base):
    """Modelo para la tabla movimientos_vigencias."""
    __tablename__ = "movimientos_vigencias"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(UUID(as_uuid=True), ForeignKey("clientes.id"), nullable=False)
    corredor_id = Column(Integer, ForeignKey("corredores.numero"))
    tipo_seguro_id = Column(Integer, ForeignKey("tipos_de_seguros.Id_tipo"), nullable=False)
    carpeta = Column(String(100))
    numero_poliza = Column(String(100), nullable=False)
    endoso = Column(String(100))
    fecha_inicio = Column(Date, nullable=False)
    fecha_vencimiento = Column(Date, nullable=False)
    moneda = Column(String(10))
    suma_asegurada = Column(Float, nullable=False)
    prima = Column(Float, nullable=False)
    comision = Column(Float)
    cuotas = Column(Integer)
    observaciones = Column(String(500))

    # Relaciones
    cliente_rel = relationship("Cliente", back_populates="movimientos_vigencias")
    corredor_rel = relationship("Corredor", back_populates="movimientos")
    tipo_seguro_rel = relationship("TipoSeguro", back_populates="movimientos")
