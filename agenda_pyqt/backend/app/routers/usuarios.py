from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta
from .. import models, schemas
from ..db.session import SessionLocal
from ..core.security import (
    authenticate_user, create_access_token, get_password_hash,
    get_current_active_user, check_admin_permission,
)
from ..core.config import settings

router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"]
)

@router.get("/verificar-primera-ejecucion", dependencies=[])
async def verificar_primera_ejecucion(db: Session = Depends(SessionLocal)):
    """Verifica si es la primera ejecución (no hay usuarios)"""
    try:
        # Verificar si existe configuración del sistema
        config = db.query(models.SystemConfig).first()
        if not config:
            # Si no existe configuración, crearla
            config = models.SystemConfig(first_run_completed=False)
            db.add(config)
            db.commit()
            return {"primera_ejecucion": True}
        
        return {"primera_ejecucion": not config.first_run_completed}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al verificar el estado del sistema: {str(e)}"
        )

@router.post("/token")
async def login_para_obtener_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(SessionLocal)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/", response_model=schemas.Usuario)
async def crear_usuario(
    usuario: schemas.UsuarioCreate,
    db: Session = Depends(SessionLocal),
    current_user: models.Usuario = Depends(check_admin_permission)
):
    # Verificar si el email ya existe
    db_user = db.query(models.Usuario).filter(models.Usuario.email == usuario.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    
    # Crear nuevo usuario
    hashed_password = get_password_hash(usuario.password)
    db_user = models.Usuario(**usuario.model_dump(exclude={'password'}), password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/mi-cuenta", response_model=schemas.Usuario)
async def obtener_usuario_actual(current_user: models.Usuario = Depends(get_current_active_user)):
    return current_user

@router.get("/", response_model=List[schemas.Usuario])
async def obtener_usuarios(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(SessionLocal),
    current_user: models.Usuario = Depends(check_admin_permission)
):
    usuarios = db.query(models.Usuario).offset(skip).limit(limit).all()
    return usuarios

@router.get("/{usuario_id}", response_model=schemas.Usuario)
async def obtener_usuario(
    usuario_id: int,
    db: Session = Depends(SessionLocal),
    current_user: models.Usuario = Depends(get_current_active_user)
):
    # Solo admins pueden ver otros usuarios
    if current_user.id != usuario_id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="No tienes permiso para ver este usuario")
    
    db_user = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_user

@router.put("/{usuario_id}", response_model=schemas.Usuario)
async def actualizar_usuario(
    usuario_id: int,
    usuario_actualizado: schemas.UsuarioUpdate,
    db: Session = Depends(SessionLocal),
    current_user: models.Usuario = Depends(get_current_active_user)
):
    # Solo admins pueden modificar otros usuarios
    if current_user.id != usuario_id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="No tienes permiso para modificar este usuario")
    
    db_user = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    update_data = usuario_actualizado.model_dump(exclude_unset=True)
    if "password" in update_data:
        update_data["password"] = get_password_hash(update_data["password"])
    
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{usuario_id}")
async def eliminar_usuario(
    usuario_id: int,
    db: Session = Depends(SessionLocal),
    current_user: models.Usuario = Depends(check_admin_permission)
):
    db_user = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db.delete(db_user)
    db.commit()
    return {"mensaje": "Usuario eliminado"}

@router.post("/configurar-admin", response_model=schemas.Usuario)
async def configurar_admin(
    usuario: schemas.UsuarioCreate,
    db: Session = Depends(SessionLocal)
):
    """Crea el usuario administrador inicial (solo funciona si no hay usuarios)"""
    try:
        # Verificar si ya existe un usuario administrador
        if db.query(models.Usuario).filter(models.Usuario.role == "admin").first():
            raise HTTPException(
                status_code=400,
                detail="Ya existe un usuario administrador"
            )
        
        # Crear el usuario administrador
        hashed_password = get_password_hash(usuario.password)
        db_user = models.Usuario(
            email=usuario.email,
            name=usuario.name,
            password=hashed_password,
            role="admin",
            is_active=True
        )
        db.add(db_user)
        
        # Marcar la configuración como completada
        config = db.query(models.SystemConfig).first()
        if not config:
            config = models.SystemConfig()
            db.add(config)
        config.first_run_completed = True
        
        db.commit()
        db.refresh(db_user)
        return db_user
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al crear usuario administrador: {str(e)}"
        )
