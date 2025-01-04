from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..db.base import Base

class TipoSeguro(Base):
    __tablename__ = "tipos_seguros"

    id = Column(Integer, primary_key=True)
    codigo = Column(String(5), nullable=False)  # Código de la cartera
    descripcion = Column(String(30), nullable=False)  # Descripción del tipo de seguro

    # Relaciones
    movimientos = relationship("MovimientoVigencia", back_populates="tipo_seguro_rel")
