"""
Endpoints relacionados con usuarios.
"""
from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ....crud import crud_usuario
from ....schemas.usuario import Usuario, UsuarioCreate, UsuarioUpdate
from ....api import deps

router = APIRouter()

@router.get("/verificar-primera-ejecucion", response_model=dict)
def verificar_primera_ejecucion(db: Session = Depends(deps.get_db)) -> Any:
    """
    Verifica si es la primera ejecución del sistema.
    Retorna True si no hay usuarios en el sistema.
    """
    usuarios = crud_usuario.get_multi(db, skip=0, limit=1)
    return {"primera_ejecucion": len(usuarios) == 0}

@router.post("/primer-administrador", response_model=Usuario)
def crear_primer_administrador(
    *,
    db: Session = Depends(deps.get_db),
    usuario_in: UsuarioCreate,
) -> Any:
    """
    Crear el primer usuario administrador del sistema.
    Este endpoint solo funciona si no hay usuarios en el sistema.
    """
    usuarios = crud_usuario.get_multi(db, skip=0, limit=1)
    if usuarios:
        raise HTTPException(
            status_code=400,
            detail="Ya existe al menos un usuario en el sistema. No se puede crear el primer administrador.",
        )
    
    # Forzar que sea superusuario y esté activo
    usuario_admin = UsuarioCreate(
        **usuario_in.model_dump(),
        is_superuser=True,
        is_active=True,
        role="admin"
    )
    
    usuario = crud_usuario.create(db, obj_in=usuario_admin)
    return usuario

@router.post("/", response_model=Usuario)
def crear_usuario(
    *,
    db: Session = Depends(deps.get_db),
    usuario_in: UsuarioCreate,
    current_user: Usuario = Depends(deps.get_usuario_activo_actual),
) -> Any:
    """
    Crear nuevo usuario.
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=400, detail="No tienes permisos suficientes"
        )
    usuario = crud_usuario.get_by_email(db, email=usuario_in.email)
    if usuario:
        raise HTTPException(
            status_code=400,
            detail="Ya existe un usuario con este email.",
        )
    usuario = crud_usuario.create(db, obj_in=usuario_in)
    return usuario

@router.get("/yo", response_model=Usuario)
def leer_usuario_actual(
    current_user: Usuario = Depends(deps.get_usuario_activo_actual),
) -> Any:
    """
    Obtener usuario actual.
    """
    return current_user

@router.put("/yo", response_model=Usuario)
def actualizar_usuario_actual(
    *,
    db: Session = Depends(deps.get_db),
    usuario_in: UsuarioUpdate,
    current_user: Usuario = Depends(deps.get_usuario_activo_actual),
) -> Any:
    """
    Actualizar usuario actual.
    """
    usuario = crud_usuario.update(db, db_obj=current_user, obj_in=usuario_in)
    return usuario
