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
    """Modelo base para clientes con validaciones de campos."""
    nombres: Optional[str] = Field(default="", max_length=100, description="Nombres del cliente")
    apellidos: str = Field(max_length=100, description="Apellidos del cliente")
    tipo_documento: str = Field(max_length=50, description="Tipo de documento de identidad")
    numero_documento: str = Field(max_length=50, description="Número de documento")
    fecha_nacimiento: date = Field(description="Fecha de nacimiento")
    direccion: str = Field(max_length=200, description="Dirección del cliente")
    localidad: Optional[str] = Field(default="", max_length=50, description="Localidad de residencia")
    telefonos: str = Field(max_length=100, description="Números de teléfono fijo")
    movil: str = Field(max_length=100, description="Número de teléfono móvil")
    mail: str = Field(max_length=100, description="Correo electrónico")
    corredor: Optional[int] = Field(default=None, description="ID del corredor asignado")
    observaciones: Optional[str] = Field(default="", max_length=500, description="Observaciones adicionales")

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
    numero_documento: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
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

class ClientePorCorredor(BaseModel):
    """Schema para mostrar información básica del cliente en listados por corredor"""
    id: UUID
    numero_cliente: int
    nombres: str
    apellidos: str
    corredor: int
    fecha_modificacion: datetime

    class Config:
        from_attributes = True
