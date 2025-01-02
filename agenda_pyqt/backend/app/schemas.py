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
    pass

class ClienteUpdate(ClienteBase):
    pass

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
