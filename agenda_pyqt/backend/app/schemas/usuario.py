"""
Schemas relacionados con la entidad Usuario.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict

from .base import validate_email, EMAIL_REGEX

class UserBase(BaseModel):
    """Modelo base para usuarios con validaciones."""
    name: str = Field(min_length=1, description="Nombre completo del usuario")
    email: str = Field(pattern=EMAIL_REGEX, description="Correo electrónico")
    role: str = Field(default="user", description="Rol del usuario")
    comision_porcentaje: float = Field(default=0.0, description="Porcentaje de comisión")

    @field_validator('email')
    @classmethod
    def validate_email_fields(cls, value):
        return validate_email(value)

    model_config = ConfigDict(from_attributes=True)

class UserCreate(UserBase):
    """Modelo para crear nuevos usuarios."""
    password: str = Field(min_length=8, description="Contraseña del usuario")

class UserUpdate(BaseModel):
    """Modelo para actualizar usuarios existentes."""
    name: Optional[str] = Field(None, min_length=1)
    email: Optional[str] = Field(None, pattern=EMAIL_REGEX)
    password: Optional[str] = Field(None, min_length=8)
    is_active: Optional[bool] = None
    role: Optional[str] = None
    comision_porcentaje: Optional[float] = None

    @field_validator('email')
    @classmethod
    def validate_email_fields(cls, value):
        return validate_email(value)

    model_config = ConfigDict(from_attributes=True)

class User(UserBase):
    """Modelo completo de usuario con campos adicionales del sistema."""
    id: int = Field(description="ID único del usuario")
    is_active: bool = Field(default=True, description="Estado del usuario")
    fecha_creacion: datetime = Field(description="Fecha de creación del registro")
    ultima_modificacion: datetime = Field(description="Fecha de última modificación")
