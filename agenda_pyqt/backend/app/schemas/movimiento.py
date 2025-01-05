"""
Schemas relacionados con la entidad MovimientoVigencia.
"""
from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, conint

class MovimientoVigenciaBase(BaseModel):
    """Modelo base para movimientos de vigencia."""
    FechaMov: date = Field(description="Fecha del movimiento")
    Corredor: int = Field(description="ID del corredor")
    Cliente: conint(gt=0) = Field(description="ID del cliente")  # Asegura que sea un entero positivo
    Tipo_seguro: int = Field(description="ID del tipo de seguro")
    Carpeta: str = Field(max_length=100, description="Carpeta del movimiento")
    Poliza: Optional[str] = Field(default=None, max_length=100, description="Póliza del movimiento")
    Endoso: Optional[str] = Field(default=None, max_length=100, description="Endoso del movimiento")
    Vto_Desde: date = Field(description="Fecha de inicio de vigencia")
    Vto_Hasta: date = Field(description="Fecha de fin de vigencia")
    Moneda: str = Field(max_length=10, description="Moneda del movimiento")
    Premio: Optional[float] = Field(default=None, description="Premio del movimiento")
    Cuotas: Optional[int] = Field(default=None, description="Número de cuotas")
    Observaciones: Optional[str] = Field(default=None, max_length=500, description="Observaciones adicionales")

    model_config = ConfigDict(from_attributes=True)

class MovimientoVigenciaCreate(MovimientoVigenciaBase):
    """Modelo para crear nuevos movimientos de vigencia."""
    pass

class MovimientoVigenciaUpdate(BaseModel):
    """Modelo para actualizar movimientos de vigencia existentes."""
    FechaMov: Optional[date] = None
    Corredor: Optional[int] = None
    Cliente: Optional[conint(gt=0)] = None
    Tipo_seguro: Optional[int] = None
    Carpeta: Optional[str] = Field(None, max_length=100)
    Poliza: Optional[str] = Field(None, max_length=100)
    Endoso: Optional[str] = Field(None, max_length=100)
    Vto_Desde: Optional[date] = None
    Vto_Hasta: Optional[date] = None
    Moneda: Optional[str] = Field(None, max_length=10)
    Premio: Optional[float] = None
    Cuotas: Optional[int] = None
    Observaciones: Optional[str] = Field(None, max_length=500)

    model_config = ConfigDict(from_attributes=True)

class MovimientoVigencia(MovimientoVigenciaBase):
    """Modelo completo de movimiento de vigencia."""
    Id_movimiento: int = Field(description="ID del movimiento")
