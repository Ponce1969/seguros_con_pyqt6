from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID

# Esquemas para User
class UserBase(BaseModel):
    name: str
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

    def __init__(self, **data):
        if 'username' not in data and 'email' in data:
            data['username'] = data['email']
        super().__init__(**data)

class UserUpdate(UserBase):
    password: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[str] = None
    comision_porcentaje: Optional[float] = None

class User(UserBase):
    id: int
    is_active: bool
    role: str
    comision_porcentaje: float
    fecha_creacion: datetime
    ultima_modificacion: datetime

    class Config:
        from_attributes = True

# Esquemas para Cliente
class ClienteBase(BaseModel):
    nombres: str
    apellidos: str
    tipo_documento: str
    documento: str
    fecha_nacimiento: datetime
    direccion: str
    localidad: Optional[str] = None
    telefonos: str
    movil: str
    email: EmailStr
    corredor: Optional[int] = None
    observaciones: Optional[str] = None

class ClienteCreate(ClienteBase):
    """
    Esquema para la creación de un cliente.
    Incluye validaciones específicas para la creación.
    """
    class Config:
        json_schema_extra = {
            "example": {
                "nombres": "Juan Carlos",
                "apellidos": "Pérez González",
                "tipo_documento": "DNI",
                "documento": "12345678",
                "fecha_nacimiento": "1990-01-01T00:00:00",
                "direccion": "Av. Principal 123",
                "localidad": "Ciudad Central",
                "telefonos": "555-1234",
                "movil": "555-5678",
                "email": "juan.perez@example.com",
                "corredor": 1,
                "observaciones": "Cliente preferencial"
            }
        }

class ClienteUpdate(ClienteBase):
    """
    Esquema para la actualización de un cliente.
    Hace todos los campos opcionales para permitir actualizaciones parciales.
    """
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    tipo_documento: Optional[str] = None
    documento: Optional[str] = None
    fecha_nacimiento: Optional[datetime] = None
    direccion: Optional[str] = None
    localidad: Optional[str] = None
    telefonos: Optional[str] = None
    movil: Optional[str] = None
    email: Optional[EmailStr] = None
    corredor: Optional[int] = None
    observaciones: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "direccion": "Nueva Dirección 456",
                "telefonos": "555-9876",
                "email": "nuevo.email@example.com"
            }
        }

class Cliente(ClienteBase):
    id: UUID
    creado_por_id: int
    modificado_por_id: int
    fecha_creacion: datetime
    fecha_modificacion: datetime

    class Config:
        from_attributes = True

# Esquemas para Token
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
