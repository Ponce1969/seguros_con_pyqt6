from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta
from .. import models, schemas
from ..database import get_db
from ..security import (
    authenticate_user, create_access_token, get_password_hash,
    get_current_active_user, check_admin_permission,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/check-first-run", dependencies=[])
async def check_first_run(db: Session = Depends(get_db)):
    """Verifica si es la primera ejecución (no hay usuarios)"""
    try:
        user_count = db.query(models.User).count()
        return {"first_run": user_count == 0}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al verificar el estado del sistema: {str(e)}"
        )

@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/", response_model=schemas.User)
async def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(check_admin_permission)
):
    # Verificar si el email ya existe
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    
    # Crear nuevo usuario
    hashed_password = get_password_hash(user.password)
    db_user = models.User(**user.model_dump(exclude={'password'}), password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/me", response_model=schemas.User)
async def read_users_me(current_user: models.User = Depends(get_current_active_user)):
    return current_user

@router.get("/", response_model=List[schemas.User])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(check_admin_permission)
):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

@router.get("/{user_id}", response_model=schemas.User)
async def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    # Solo admins pueden ver otros usuarios
    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="No tienes permiso para ver este usuario")
    
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_user

@router.put("/{user_id}", response_model=schemas.User)
async def update_user(
    user_id: int,
    user_update: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    # Solo admins pueden modificar otros usuarios
    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="No tienes permiso para modificar este usuario")
    
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    update_data = user_update.model_dump(exclude_unset=True)
    if "password" in update_data:
        update_data["password"] = get_password_hash(update_data["password"])
    
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(check_admin_permission)
):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db.delete(db_user)
    db.commit()
    return {"message": "Usuario eliminado"}

@router.post("/setup-admin", response_model=schemas.User)
async def setup_admin(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    """Crea el usuario administrador inicial (solo funciona si no hay usuarios)"""
    try:
        # Verificar si ya hay usuarios
        user_count = db.query(models.User).count()
        if user_count > 0:
            raise HTTPException(
                status_code=400,
                detail="La configuración inicial ya fue realizada"
            )
        
        # Validar que el usuario tenga todos los campos requeridos
        if not user.name or not user.email or not user.password:
            raise HTTPException(
                status_code=400,
                detail="Faltan campos requeridos (nombre, email o contraseña)"
            )
        
        # Verificar si el email ya existe (por si acaso)
        existing_user = db.query(models.User).filter(models.User.email == user.email).first()
        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="El email ya está registrado"
            )
        
        # Crear usuario admin
        hashed_password = get_password_hash(user.password)
        db_user = models.User(
            name=user.name,
            email=user.email,
            password=hashed_password,
            role="admin",
            comision_porcentaje=0.0,
            is_active=True
        )
        
        try:
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return db_user
        except Exception as e:
            db.rollback()
            print(f"Error al guardar en la base de datos: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error al guardar en la base de datos: {str(e)}"
            )
        
    except HTTPException as he:
        raise he
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error al crear admin: {str(e)}\n{error_details}")
        raise HTTPException(
            status_code=500,
            detail=f"Error al crear el usuario administrador: {str(e)}"
        )
