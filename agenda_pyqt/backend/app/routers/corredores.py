from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..db.session import get_db
from sqlalchemy.exc import IntegrityError

router = APIRouter()

@router.post("/", response_model=schemas.Corredor, status_code=status.HTTP_201_CREATED)
def create_corredor(corredor: schemas.CorredorCreate, db: Session = Depends(get_db)):
    """Crear un nuevo corredor"""
    try:
        # Verificar si ya existe un corredor con ese número
        db_corredor = db.query(models.Corredor).filter(models.Corredor.numero == corredor.numero).first()
        if db_corredor:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un corredor con el número {corredor.numero}"
            )
        
        # Verificar si ya existe un corredor con ese documento
        db_corredor = db.query(models.Corredor).filter(models.Corredor.documento == corredor.documento).first()
        if db_corredor:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un corredor con el documento {corredor.documento}"
            )

        db_corredor = models.Corredor(**corredor.model_dump())
        db.add(db_corredor)
        db.commit()
        db.refresh(db_corredor)
        return db_corredor
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error de integridad en los datos. Verifica que no haya duplicados."
        )

@router.get("/", response_model=List[schemas.Corredor])
def read_corredores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener lista de corredores"""
    corredores = db.query(models.Corredor).offset(skip).limit(limit).all()
    return corredores

@router.get("/{numero}", response_model=schemas.Corredor)
def read_corredor(numero: int, db: Session = Depends(get_db)):
    """Obtener un corredor por su número"""
    db_corredor = db.query(models.Corredor).filter(models.Corredor.numero == numero).first()
    if db_corredor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró el corredor con número {numero}"
        )
    return db_corredor

@router.put("/{numero}", response_model=schemas.Corredor)
def update_corredor(numero: int, corredor: schemas.CorredorUpdate, db: Session = Depends(get_db)):
    """Actualizar un corredor"""
    try:
        db_corredor = db.query(models.Corredor).filter(models.Corredor.numero == numero).first()
        if db_corredor is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró el corredor con número {numero}"
            )

        # Actualizar solo los campos que no son None
        corredor_data = corredor.model_dump(exclude_unset=True)
        for key, value in corredor_data.items():
            setattr(db_corredor, key, value)

        db.commit()
        db.refresh(db_corredor)
        return db_corredor
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error de integridad en los datos. Verifica que no haya duplicados."
        )

@router.delete("/{numero}", status_code=status.HTTP_204_NO_CONTENT)
def delete_corredor(numero: int, db: Session = Depends(get_db)):
    """Eliminar un corredor"""
    db_corredor = db.query(models.Corredor).filter(models.Corredor.numero == numero).first()
    if db_corredor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró el corredor con número {numero}"
        )
    
    try:
        db.delete(db_corredor)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar el corredor porque tiene movimientos asociados"
        )
    return None
