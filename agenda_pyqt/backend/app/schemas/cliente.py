"""
Schemas relacionados con la entidad Cliente.
"""
from datetime import date, datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field, field_validator, ConfigDict

from .base import validate_phone, validate_email, EMAIL_REGEX
from .movimiento import MovimientoVigencia

class ClienteBase(BaseModel):
    """Modelo base para clientes con validaciones de campos."""
    nombres: Optional[str] = Field(default="", max_length=100, description="Nombres del cliente")
    apellidos: str = Field(max_length=100, description="Apellidos del cliente")
    tipo_documento: Optional[str] = Field(default=None, description="Tipo de documento de identidad")
    documentos: Optional[str] = Field(default="", max_length=50, description="Número de documento")
    fecha_nacimiento: Optional[date] = Field(default=None, description="Fecha de nacimiento")
    direccion: str = Field(max_length=200, description="Dirección del cliente")
    localidad: Optional[str] = Field(default="", max_length=50, description="Localidad de residencia")
    telefonos: Optional[str] = Field(default="", max_length=100, description="Números de teléfono fijo")
    movil: Optional[str] = Field(default="", max_length=100, description="Número de teléfono móvil")
    mail: Optional[str] = Field(default="", max_length=100, description="Correo electrónico")
    corredor: Optional[int] = Field(default=None, description="ID del corredor asignado")
    observaciones: Optional[str] = Field(default="", max_length=500, description="Observaciones adicionales")

    @field_validator('telefonos', 'movil')
    @classmethod
    def validate_phone_fields(cls, value):
        return validate_phone(value)

    @field_validator('mail')
    @classmethod
    def validate_email_fields(cls, value):
        return validate_email(value)

    model_config = ConfigDict(from_attributes=True)

class ClienteCreate(ClienteBase):
    """Modelo para crear nuevos clientes."""
    pass

class ClienteUpdate(ClienteBase):
    """Modelo para actualizar clientes existentes."""
    nombres: Optional[str] = Field(None, max_length=100)
    apellidos: Optional[str] = Field(None, max_length=100)
    direccion: Optional[str] = Field(None, max_length=200)

class Cliente(ClienteBase):
    """Modelo completo de cliente con campos adicionales del sistema."""
    id: UUID = Field(description="ID único del cliente")
    creado_por_id: int = Field(description="ID del usuario que creó el registro")
    modificado_por_id: int = Field(description="ID del usuario que modificó el registro")
    fecha_creacion: datetime = Field(description="Fecha de creación del registro")
    fecha_modificacion: datetime = Field(description="Fecha de última modificación")
    movimientos_vigencias: List[MovimientoVigencia] = Field(default_factory=list, description="Movimientos de vigencia asociados")
