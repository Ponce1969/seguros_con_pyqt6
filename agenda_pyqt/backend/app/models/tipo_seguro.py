from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..db.base import Base

class TipoSeguro(Base):
    __tablename__ = "tipos_de_seguros"

    Id_tipo = Column(Integer, primary_key=True)
    Aseguradora = Column(String(15), nullable=False)
    Codigo = Column(String(5), nullable=False)
    Descripcion = Column(String(30), nullable=False)

    # Relaciones
    movimientos = relationship("MovimientoVigencia", back_populates="tipo_seguro_rel")
