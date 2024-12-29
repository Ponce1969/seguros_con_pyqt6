"""
Schemas relacionados con la entidad Corredor.
"""
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator, ConfigDict

from .base import validate_phone, validate_email, EMAIL_REGEX, PHONE_REGEX
from .movimiento import MovimientoVigencia

class CorredorBase(BaseModel):
    """Modelo base para corredores."""
    nombres: Optional[str] = Field(default=None, max_length=30, description="Nombres del corredor")
    apellidos: str = Field(min_length=1, max_length=30, description="Apellidos del corredor")
    documento: str = Field(min_length=1, max_length=20, description="Número de documento")
    direccion: str = Field(min_length=1, max_length=70, description="Dirección del corredor")
    localidad: str = Field(min_length=1, max_length=15, description="Localidad de residencia")
    telefonos: Optional[str] = Field(default=None, pattern=PHONE_REGEX, description="Números de teléfono fijo")
    movil: Optional[str] = Field(default=None, pattern=PHONE_REGEX, description="Número de teléfono móvil")
    mail: str = Field(pattern=EMAIL_REGEX, description="Correo electrónico")
    observaciones: Optional[str] = Field(default=None, description="Observaciones adicionales")

    @field_validator('telefonos', 'movil')
    @classmethod
    def validate_phone_fields(cls, value):
        return validate_phone(value)

    @field_validator('mail')
    @classmethod
    def validate_email_fields(cls, value):
        return validate_email(value)

    model_config = ConfigDict(from_attributes=True)

class CorredorCreate(CorredorBase):
    """Modelo para crear nuevos corredores."""
    numero: int = Field(gt=0, description="Número de corredor")

class CorredorUpdate(BaseModel):
    """Modelo para actualizar corredores existentes."""
    nombres: Optional[str] = Field(None, max_length=30)
    apellidos: Optional[str] = Field(None, min_length=1, max_length=30)
    documento: Optional[str] = Field(None, min_length=1, max_length=20)
    direccion: Optional[str] = Field(None, min_length=1, max_length=70)
    localidad: Optional[str] = Field(None, min_length=1, max_length=15)
    telefonos: Optional[str] = Field(None, pattern=PHONE_REGEX)
    movil: Optional[str] = Field(None, pattern=PHONE_REGEX)
    mail: Optional[str] = Field(None, pattern=EMAIL_REGEX)
    observaciones: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class Corredor(CorredorBase):
    """Modelo completo de corredor."""
    numero: int = Field(description="Número de corredor")
    movimientos: List[MovimientoVigencia] = Field(default_factory=list, description="Movimientos de vigencia asociados")
