"""
Esquemas Pydantic para usuarios.
"""
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime

class UsuarioBase(BaseModel):
    """Esquema base para usuarios"""
    email: Optional[EmailStr] = Field(None, description="Correo electrónico")
    is_active: Optional[bool] = Field(True, description="Estado del usuario")
    is_superuser: bool = Field(False, description="Es superusuario")
    nombre: Optional[str] = Field(None, description="Nombre")
    apellido: Optional[str] = Field(None, description="Apellido")
    username: Optional[str] = Field(None, description="Nombre de usuario")
    role: Optional[str] = Field(None, description="Rol del usuario")
    comision_porcentaje: Optional[float] = Field(0.0, description="Porcentaje de comisión")

    model_config = ConfigDict(from_attributes=True)

class UsuarioCreate(UsuarioBase):
    """Esquema para crear usuarios"""
    email: EmailStr = Field(description="Correo electrónico")
    password: str = Field(min_length=8, description="Contraseña del usuario")
    nombre: str = Field(description="Nombre")
    apellido: str = Field(description="Apellido")
    username: str = Field(min_length=3, description="Nombre de usuario")
    role: str = Field(default="user", description="Rol del usuario")

class UsuarioUpdate(UsuarioBase):
    """Esquema para actualizar usuarios"""
    password: Optional[str] = Field(None, min_length=8, description="Contraseña del usuario")

    model_config = ConfigDict(from_attributes=True)

class Usuario(UsuarioBase):
    """Esquema para respuestas de usuario"""
    id: int = Field(description="ID único del usuario")
    fecha_creacion: datetime = Field(description="Fecha de creación del registro")
    fecha_modificacion: datetime = Field(description="Fecha de última modificación")
    is_active: bool = Field(description="Estado del usuario")
    is_superuser: bool = Field(description="Es superusuario")

    model_config = ConfigDict(from_attributes=True)

# Alias para mantener compatibilidad con código existente
UserBase = UsuarioBase
UserCreate = UsuarioCreate
UserUpdate = UsuarioUpdate
User = Usuario
