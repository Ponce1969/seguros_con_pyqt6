from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
import logging

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

@router.post("/", response_model=schemas.MovimientoVigencia)
def create_movimiento(movimiento: schemas.MovimientoVigenciaCreate, db: Session = Depends(get_db)):
    try:
        # Verificar si el cliente existe
        cliente = db.query(models.Cliente).filter(models.Cliente.id == movimiento.cliente_id).first()
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")

        db_movimiento = models.MovimientoVigencia(**movimiento.dict())
        db.add(db_movimiento)
        db.commit()
        db.refresh(db_movimiento)
        return db_movimiento
    except Exception as e:
        logger.error(f"Error al crear movimiento: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[schemas.MovimientoVigencia])
def read_movimientos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    movimientos = db.query(models.MovimientoVigencia).offset(skip).limit(limit).all()
    return movimientos

@router.get("/{movimiento_id}", response_model=schemas.MovimientoVigencia)
def read_movimiento(movimiento_id: int, db: Session = Depends(get_db)):
    db_movimiento = db.query(models.MovimientoVigencia).filter(models.MovimientoVigencia.id == movimiento_id).first()
    if db_movimiento is None:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")
    return db_movimiento

@router.get("/cliente/{cliente_id}", response_model=List[schemas.MovimientoVigencia])
def read_movimientos_by_cliente(cliente_id: UUID, db: Session = Depends(get_db)):
    # Verificar si el cliente existe
    cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    movimientos = db.query(models.MovimientoVigencia).filter(models.MovimientoVigencia.cliente_id == cliente_id).all()
    return movimientos

@router.put("/{movimiento_id}", response_model=schemas.MovimientoVigencia)
def update_movimiento(movimiento_id: int, movimiento: schemas.MovimientoVigenciaCreate, db: Session = Depends(get_db)):
    db_movimiento = db.query(models.MovimientoVigencia).filter(models.MovimientoVigencia.id == movimiento_id).first()
    if db_movimiento is None:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")
    
    for key, value in movimiento.dict().items():
        setattr(db_movimiento, key, value)
    db.commit()
    return db_movimiento

@router.delete("/{movimiento_id}")
def delete_movimiento(
    movimiento_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    db_movimiento = db.query(models.MovimientoVigencia).filter(models.MovimientoVigencia.id == movimiento_id).first()
    if db_movimiento is None:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")
    
    db.delete(db_movimiento)
    db.commit()
    return {"message": "Movimiento eliminado"}
