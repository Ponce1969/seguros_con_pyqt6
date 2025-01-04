from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
import logging
import traceback

from ..db.session import SessionLocal
from .. import models, schemas
from ..core.security import get_current_active_user

# Configurar logging
logger = logging.getLogger(__name__)

router = APIRouter()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Cliente, status_code=201)
def create_cliente(
    cliente: schemas.ClienteCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    try:
        logger.debug(f"Datos recibidos: {cliente.model_dump()}")
        # Crear el cliente con los IDs del usuario actual
        db_cliente = models.Cliente(
            **cliente.dict(),
            creado_por_id=current_user.id,
            modificado_por_id=current_user.id
        )
        db.add(db_cliente)
        db.commit()
        db.refresh(db_cliente)
        logger.debug(f"Cliente creado: {db_cliente.id}")
        return db_cliente
    except Exception as e:
        logger.error(f"Error al crear cliente: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error al crear el cliente: {str(e)}")

@router.get("/", response_model=List[schemas.Cliente])
def read_clientes(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    try:
        clientes = db.query(models.Cliente).offset(skip).limit(limit).all()
        return clientes
    except Exception as e:
        logger.error(f"Error al obtener clientes: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{cliente_id}", response_model=schemas.Cliente)
def read_cliente(
    cliente_id: UUID, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    db_cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return db_cliente

@router.put("/{cliente_id}", response_model=schemas.Cliente)
def update_cliente(
    cliente_id: UUID, 
    cliente_actualizado: schemas.ClienteUpdate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    try:
        db_cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
        if db_cliente is None:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        
        # Actualizar los campos del cliente
        for key, value in cliente_actualizado.dict(exclude_unset=True).items():
            setattr(db_cliente, key, value)
        
        # Actualizar el ID del usuario que modifica
        db_cliente.modificado_por_id = current_user.id
        
        db.commit()
        db.refresh(db_cliente)
        return db_cliente
    except Exception as e:
        logger.error(f"Error al actualizar cliente: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{cliente_id}")
def delete_cliente(
    cliente_id: UUID, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    db_cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    db.delete(db_cliente)
    db.commit()
    return {"message": "Cliente eliminado"}
