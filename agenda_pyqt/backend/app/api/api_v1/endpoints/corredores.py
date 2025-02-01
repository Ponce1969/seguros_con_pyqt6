from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ....db.session import get_db
from .... import models, schemas
from ....core.security import get_current_user

router = APIRouter()

@router.post("/", response_model=schemas.Corredor)
def create_corredor(
    corredor: schemas.CorredorCreate,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user)
):
    """Crear un nuevo corredor"""
    # Verificar si ya existe un corredor con ese número
    db_corredor = db.query(models.Corredor).filter(models.Corredor.numero == corredor.numero).first()
    if db_corredor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un corredor con el número {corredor.numero}"
        )
    
    # Crear el nuevo corredor
    db_corredor = models.Corredor(**corredor.model_dump())
    db.add(db_corredor)
    db.commit()
    db.refresh(db_corredor)
    return db_corredor

@router.get("/", response_model=List[schemas.Corredor])
def read_corredores(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user)
):
    """Obtener lista de corredores"""
    corredores = db.query(models.Corredor).offset(skip).limit(limit).all()
    return [
        schemas.Corredor(
            numero=corredor.numero,
            nombres=corredor.nombres,
            apellidos=corredor.apellidos,
            documento=corredor.documento,
            direccion=corredor.direccion,
            localidad=corredor.localidad,
            telefonos=corredor.telefonos,
            movil=corredor.movil,
            mail=corredor.mail,
            observaciones=corredor.observaciones,
            movimientos=[]  # Lista vacía por defecto
        )
        for corredor in corredores
    ]

@router.get("/{numero}", response_model=schemas.Corredor)
def read_corredor(
    numero: int,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user)
):
    """Obtener un corredor específico por su número"""
    corredor = db.query(models.Corredor).filter(models.Corredor.numero == numero).first()
    if corredor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró el corredor con número {numero}"
        )
    return corredor

@router.put("/{numero}", response_model=schemas.Corredor)
def update_corredor(
    numero: int,
    corredor: schemas.CorredorUpdate,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user)
):
    """Actualizar un corredor existente"""
    db_corredor = db.query(models.Corredor).filter(models.Corredor.numero == numero).first()
    if db_corredor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró el corredor con número {numero}"
        )
    
    # Actualizar los campos del corredor
    for key, value in corredor.model_dump(exclude_unset=True).items():
        setattr(db_corredor, key, value)
    
    db.commit()
    db.refresh(db_corredor)
    return db_corredor

@router.delete("/{numero}", response_model=schemas.Corredor)
def delete_corredor(
    numero: int,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user)
):
    """Eliminar un corredor"""
    db_corredor = db.query(models.Corredor).filter(models.Corredor.numero == numero).first()
    if db_corredor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró el corredor con número {numero}"
        )
    
    db.delete(db_corredor)
    db.commit()
    return db_corredor
