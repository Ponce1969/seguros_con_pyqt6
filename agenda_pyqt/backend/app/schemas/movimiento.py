"""
Schemas relacionados con la entidad MovimientoVigencia.
"""
from datetime import date
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict

class MovimientoVigenciaBase(BaseModel):
    """Modelo base para movimientos de vigencia."""
    fecha_mov: date = Field(description="Fecha del movimiento")
    corredor: int = Field(description="ID del corredor")
    numero_cliente_compania: Optional[str] = Field(default=None, max_length=100, description="Número de cliente en la compañía")
    tipo_seguro: int = Field(description="ID del tipo de seguro")
    carpeta: str = Field(max_length=100, description="Carpeta del movimiento")
    poliza: Optional[str] = Field(default=None, max_length=100, description="Póliza del movimiento")
    endoso: Optional[str] = Field(default=None, max_length=100, description="Endoso del movimiento")
    vto_desde: date = Field(description="Fecha de inicio de vigencia")
    vto_hasta: date = Field(description="Fecha de fin de vigencia")
    moneda: str = Field(max_length=10, description="Moneda del movimiento")
    premio: Optional[float] = Field(default=None, description="Premio del movimiento")
    cuotas: Optional[int] = Field(default=None, description="Número de cuotas")
    observaciones: Optional[str] = Field(default=None, max_length=500, description="Observaciones adicionales")

    model_config = ConfigDict(from_attributes=True)

class MovimientoVigenciaCreate(MovimientoVigenciaBase):
    """Modelo para crear nuevos movimientos de vigencia."""
    cliente_id: UUID = Field(description="ID del cliente")

class MovimientoVigencia(MovimientoVigenciaBase):
    """Modelo completo de movimiento de vigencia."""
    id_movimiento: int = Field(description="ID del movimiento")
    cliente_id: UUID = Field(description="ID del cliente")
