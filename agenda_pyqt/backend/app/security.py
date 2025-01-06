from datetime import datetime, timedelta
from typing import Optional, Union
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import os
from . import models, schemas
from .database import get_db

# Configuración de seguridad desde variables de entorno
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    # En desarrollo, usar una clave por defecto (NO HACER ESTO EN PRODUCCIÓN)
    if os.getenv("ENVIRONMENT", "development") == "development":
        SECRET_KEY = "wVUQdvQpeIAe7i-qc4mq5gLR2Ndn06FlafJKCTQhHCZ2wY7ky3_42n1ELvWjehz2exkKeDsGegst9FPZYJLUFA"
    else:
        raise ValueError("No se ha configurado SECRET_KEY en las variables de entorno")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))

# Configuración de seguridad para contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuración OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")

class AuthenticationError(Exception):
    """Excepción personalizada para errores de autenticación"""
    def __init__(self, detail: str):
        self.detail = detail

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si una contraseña sin cifrar coincide con la contraseña cifrada.
    
    Args:
        plain_password: Contraseña sin cifrar
        hashed_password: Contraseña cifrada
    
    Returns:
        bool: True si las contraseñas coinciden, False en caso contrario
    """
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False

def get_password_hash(password: str) -> str:
    """
    Cifra la contraseña utilizando bcrypt.
    
    Args:
        password: Contraseña a cifrar
    
    Returns:
        str: Contraseña cifrada
    
    Raises:
        ValueError: Si la contraseña está vacía o es None
    """
    if not password:
        raise ValueError("La contraseña no puede estar vacía")
    return pwd_context.hash(password)

def authenticate_user(db: Session, email: str, password: str) -> models.User:
    """
    Autentica al usuario buscando por email y verificando la contraseña.
    
    Args:
        db: Sesión de base de datos
        email: Email del usuario
        password: Contraseña sin cifrar
    
    Returns:
        models.User: Usuario autenticado
    
    Raises:
        HTTPException: Si el usuario no existe o la contraseña es incorrecta
    """
    if not email or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email y contraseña son requeridos"
        )
    
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        # Usar tiempo constante para evitar timing attacks
        pwd_context.verify("dummy", get_password_hash("dummy"))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )
    
    if not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )
    
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crea un token de acceso JWT.
    
    Args:
        data: Datos a codificar en el token
        expires_delta: Tiempo de expiración opcional
    
    Returns:
        str: Token JWT codificado
    """
    to_encode = data.copy()
    expire = datetime.now(datetime.timezone.utc) + (
        expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({
        "exp": expire,
        "iat": datetime.now(datetime.timezone.utc)  # Tiempo de emisión del token
    })
    
    try:
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al generar el token"
        )

async def get_current_user(
    request: Request,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> models.User:
    """
    Obtiene al usuario actual a partir del token de acceso.
    
    Args:
        request: Objeto Request de FastAPI
        token: Token JWT
        db: Sesión de base de datos
    
    Returns:
        models.User: Usuario actual
    
    Raises:
        HTTPException: Si el token es inválido o el usuario no existe
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if not email:
            raise credentials_exception
            
        # Verificar tiempo de expiración
        exp = payload.get("exp")
        if not exp or datetime.fromtimestamp(exp, tz=datetime.timezone.utc) < datetime.now(datetime.timezone.utc):
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception
    
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise credentials_exception
        
    # Almacenar información del usuario en el request para logging
    request.state.user = user
    return user

async def get_current_active_user(
    current_user: models.User = Depends(get_current_user)
) -> models.User:
    """
    Verifica si el usuario está activo.
    
    Args:
        current_user: Usuario actual
    
    Returns:
        models.User: Usuario activo
    
    Raises:
        HTTPException: Si el usuario está inactivo
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )
    return current_user

def check_admin_permission(
    current_user: models.User = Depends(get_current_active_user)
) -> models.User:
    """
    Verifica si el usuario tiene permisos de administrador.
    
    Args:
        current_user: Usuario actual
    
    Returns:
        models.User: Usuario administrador
    
    Raises:
        HTTPException: Si el usuario no tiene permisos de administrador
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requieren permisos de administrador para esta operación"
        )
    return current_user
