"""
Endpoints para autenticación e inicio de sesión.
"""
from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ....core import security
from ....core.config import settings
from ....core.security import get_password_hash
from .... import crud
from ....schemas.token import Token
from ....api import deps

router = APIRouter()

@router.post("/iniciar-sesion/token", response_model=Token)
def obtener_token_acceso(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, obtiene un token de acceso para futuras peticiones.
    """
    usuario = crud.crud_usuario.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not usuario:
        raise HTTPException(status_code=400, detail="Email o contraseña incorrectos")
    elif not usuario.is_active:
        raise HTTPException(status_code=400, detail="Usuario inactivo")
    
    expiracion_token = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            {"sub": str(usuario.id)},  
            expires_delta=expiracion_token
        ),
        "token_type": "bearer",
    }
