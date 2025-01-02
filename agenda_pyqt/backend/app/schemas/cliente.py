"""
Schemas relacionados con la entidad Cliente.
"""
from datetime import date, datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field, field_validator, ConfigDict, constr

from .base import validate_phone, validate_email
from .movimiento import MovimientoVigencia

class ClienteBase(BaseModel):
    """Schema base para clientes."""
    nombres: Optional[str] = Field(default="", max_length=100)
    apellidos: str = Field(max_length=100)
    tipo_documento: Optional[str] = Field(default=None, max_length=50)
    documento: Optional[str] = Field(default="", max_length=50)
    fecha_nacimiento: Optional[date] = None
    direccion: str = Field(max_length=200)
    localidad: Optional[str] = Field(default="", max_length=50)
    telefonos: Optional[str] = Field(default="", max_length=100)
    movil: Optional[str] = Field(default="", max_length=100)
    mail: Optional[str] = Field(default="", max_length=100)
    corredor: Optional[int] = None
    observaciones: Optional[str] = None

    @field_validator('telefonos', 'movil')
    def validate_phone(cls, v):
        if v:
            return validate_phone(v)
        return v

    @field_validator('mail')
    def validate_email(cls, v):
        if v:
            return validate_email(v)
        return v

    model_config = ConfigDict(from_attributes=True)

class ClienteCreate(ClienteBase):
    """Schema para crear clientes."""
    apellidos: constr(min_length=2, max_length=100)
    direccion: constr(min_length=5, max_length=200)

class ClienteUpdate(BaseModel):
    """Schema para actualizar clientes."""
    nombres: Optional[str] = Field(None, max_length=100)
    apellidos: Optional[str] = Field(None, max_length=100)
    direccion: Optional[str] = Field(None, max_length=200)
    tipo_documento: Optional[str] = None
    documento: Optional[str] = None
    localidad: Optional[str] = None
    telefonos: Optional[str] = None
    movil: Optional[str] = None
    mail: Optional[str] = None
    corredor: Optional[int] = None
    observaciones: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class Cliente(ClienteBase):
    """Schema completo de cliente."""
    id: UUID
    numero_cliente: int
    creado_por_id: int
    modificado_por_id: int
    fecha_creacion: datetime
    fecha_modificacion: datetime
    movimientos_vigencias: List[MovimientoVigencia] = []

    model_config = ConfigDict(from_attributes=True)
