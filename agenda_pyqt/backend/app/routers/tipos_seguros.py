from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..db.session import get_db
from .. import models, schemas

router = APIRouter(
    prefix="/tipos-seguros",
    tags=["tipos_seguros"]
)

@router.post("/", response_model=schemas.TipoSeguro)
def create_tipo_seguro(tipo_seguro: schemas.TipoSeguroCreate, db: Session = Depends(get_db)):
    db_tipo = models.TipoSeguro(**tipo_seguro.model_dump())
    db.add(db_tipo)
    db.commit()
    db.refresh(db_tipo)
    return db_tipo

@router.get("/", response_model=List[schemas.TipoSeguro])
def read_tipos_seguros(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tipos = db.query(models.TipoSeguro).offset(skip).limit(limit).all()
    return tipos

@router.get("/{id_tipo}", response_model=schemas.TipoSeguro)
def read_tipo_seguro(id_tipo: int, db: Session = Depends(get_db)):
    db_tipo = db.query(models.TipoSeguro).filter(models.TipoSeguro.id_tipo == id_tipo).first()
    if db_tipo is None:
        raise HTTPException(status_code=404, detail="Tipo de seguro no encontrado")
    return db_tipo

@router.put("/{id_tipo}", response_model=schemas.TipoSeguro)
def update_tipo_seguro(id_tipo: int, tipo_seguro: schemas.TipoSeguroUpdate, db: Session = Depends(get_db)):
    db_tipo = db.query(models.TipoSeguro).filter(models.TipoSeguro.id_tipo == id_tipo).first()
    if db_tipo is None:
        raise HTTPException(status_code=404, detail="Tipo de seguro no encontrado")
    
    update_data = tipo_seguro.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_tipo, field, value)
    
    db.commit()
    db.refresh(db_tipo)
    return db_tipo

@router.delete("/{id_tipo}")
def delete_tipo_seguro(id_tipo: int, db: Session = Depends(get_db)):
    db_tipo = db.query(models.TipoSeguro).filter(models.TipoSeguro.id_tipo == id_tipo).first()
    if db_tipo is None:
        raise HTTPException(status_code=404, detail="Tipo de seguro no encontrado")
    
    db.delete(db_tipo)
    db.commit()
    return {"message": "Tipo de seguro eliminado"}
