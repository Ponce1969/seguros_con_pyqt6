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
        # Buscar el cliente por su número
        cliente = db.query(models.Cliente).filter(models.Cliente.numero_cliente == movimiento.Cliente).first()
        if not cliente:
            raise HTTPException(status_code=404, detail=f"Cliente número {movimiento.Cliente} no encontrado")

        # Crear el movimiento con los campos correctos
        db_movimiento = models.MovimientoVigencia(
            cliente_id=cliente.id,  # UUID del cliente
            corredor_id=movimiento.Corredor,
            tipo_seguro_id=movimiento.Tipo_seguro,
            carpeta=movimiento.Carpeta,
            numero_poliza=movimiento.Poliza,
            endoso=movimiento.Endoso,
            fecha_inicio=movimiento.Vto_Desde,
            fecha_vencimiento=movimiento.Vto_Hasta,
            moneda=movimiento.Moneda,
            suma_asegurada=movimiento.Premio,  # Asumiendo que Premio es la suma asegurada
            prima=movimiento.Premio,  # Asumiendo que Premio es también la prima
            cuotas=movimiento.Cuotas,
            observaciones=movimiento.Observaciones
        )
        
        db.add(db_movimiento)
        db.commit()
        db.refresh(db_movimiento)

        # Crear el objeto MovimientoVigencia con el nombre del cliente
        return schemas.MovimientoVigencia(
            Id_movimiento=db_movimiento.id,
            FechaMov=movimiento.FechaMov,
            Corredor=movimiento.Corredor,
            Cliente=movimiento.Cliente,
            Cliente_nombre=f"{cliente.nombres} {cliente.apellidos}",  # Agregamos el nombre del cliente
            Tipo_seguro=movimiento.Tipo_seguro,
            Carpeta=movimiento.Carpeta,
            Poliza=movimiento.Poliza,
            Endoso=movimiento.Endoso,
            Vto_Desde=movimiento.Vto_Desde,
            Vto_Hasta=movimiento.Vto_Hasta,
            Moneda=movimiento.Moneda,
            Premio=movimiento.Premio,
            Cuotas=movimiento.Cuotas,
            Observaciones=movimiento.Observaciones
        )

    except Exception as e:
        logger.error(f"Error al crear movimiento: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[schemas.MovimientoVigencia])
def read_movimientos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    movimientos = db.query(models.MovimientoVigencia).offset(skip).limit(limit).all()
    
    # Transformar los movimientos al formato esperado por el frontend
    return [
        schemas.MovimientoVigencia(
            Id_movimiento=mov.id,
            FechaMov=mov.fecha_inicio,
            Corredor=mov.corredor_id,
            Cliente=mov.cliente_rel.numero_cliente,
            Cliente_nombre=f"{mov.cliente_rel.nombres} {mov.cliente_rel.apellidos}",
            Tipo_seguro=mov.tipo_seguro_id,
            Carpeta=mov.carpeta,
            Poliza=mov.numero_poliza,
            Endoso=mov.endoso,
            Vto_Desde=mov.fecha_inicio,
            Vto_Hasta=mov.fecha_vencimiento,
            Moneda=mov.moneda,
            Premio=mov.prima,
            Cuotas=mov.cuotas,
            Observaciones=mov.observaciones
        ) 
        for mov in movimientos
    ]

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
