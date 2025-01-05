"""
Dependencias para los endpoints de la API.
"""
from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from ..core.config import settings
from ..core import security
from ..crud.crud_usuario import crud_usuario
from ..models.usuario import Usuario
from ..schemas.token import TokenPayload
from ..db.session import SessionLocal

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)

def get_db() -> Generator:
    """
    Dependencia para obtener una sesión de base de datos.
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_usuario_actual(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> Usuario:
    """
    Dependencia para obtener el usuario actual a partir del token JWT.
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No se pudo validar las credenciales",
        )
    usuario = crud_usuario.get(db, id=token_data.sub)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

def get_usuario_activo_actual(
    usuario_actual: Usuario = Depends(get_usuario_actual),
) -> Usuario:
    """
    Dependencia para obtener el usuario actual activo.
    """
    if not usuario_actual.is_active:
        raise HTTPException(status_code=400, detail="Usuario inactivo")
    return usuario_actual
