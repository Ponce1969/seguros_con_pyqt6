from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from ..db.base import Base

class MovimientoVigencia(Base):
    __tablename__ = "movimientos_vigencia"

    id = Column(Integer, primary_key=True)
    cliente_id = Column(UUID(as_uuid=True), ForeignKey("clientes.id"), nullable=False)
    corredor_id = Column(Integer, ForeignKey("corredores.numero"))
    tipo_seguro_id = Column(Integer, ForeignKey("tipos_seguros.id"), nullable=False)
    numero_poliza = Column(String(20), nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_vencimiento = Column(Date, nullable=False)
    suma_asegurada = Column(Float, nullable=False)
    prima = Column(Float, nullable=False)
    comision = Column(Float)
    cuotas = Column(Integer)
    observaciones = Column(Text)

    # Relaciones
    cliente_rel = relationship("Cliente", back_populates="movimientos_vigencias")
    corredor_rel = relationship("Corredor", back_populates="movimientos")
    tipo_seguro_rel = relationship("TipoSeguro", back_populates="movimientos")
