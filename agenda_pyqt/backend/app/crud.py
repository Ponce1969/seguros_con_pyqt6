from sqlalchemy.orm import Session
from . import models, schemas
from uuid import UUID

# Obtener un cliente por ID
def get_cliente(db: Session, cliente_id: UUID):
    return db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()

# Obtener un cliente por documento
def get_cliente_by_documento(db: Session, documento: str):
    return db.query(models.Cliente).filter(models.Cliente.documentos == documento).first()

# Obtener lista de clientes
def get_clientes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Cliente).offset(skip).limit(limit).all()

# Crear un nuevo cliente
def create_cliente(db: Session, cliente: schemas.ClienteCreate):
    db_cliente = models.Cliente(**cliente.dict())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

# Actualizar un cliente existente
def update_cliente(db: Session, cliente_id: UUID, cliente: schemas.ClienteUpdate):
    db_cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
    if db_cliente:
        for key, value in cliente.dict(exclude_unset=True).items():
            setattr(db_cliente, key, value)
        db.commit()
        db.refresh(db_cliente)
    return db_cliente

# Eliminar un cliente
def delete_cliente(db: Session, cliente_id: UUID):
    db_cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
    if db_cliente:
        db.delete(db_cliente)
        db.commit()
    return db_cliente

# Funciones CRUD para MovimientoVigencia
def create_movimiento_vigencia(db: Session, movimiento: schemas.MovimientoVigenciaCreate):
    try:
        movimiento_data = movimiento.model_dump()
        db_movimiento = models.MovimientoVigencia(**movimiento_data)
        db.add(db_movimiento)
        db.commit()
        db.refresh(db_movimiento)
        return db_movimiento
    except Exception as e:
        db.rollback()
        raise e

def get_movimiento_vigencia(db: Session, movimiento_id: int):
    return db.query(models.MovimientoVigencia).filter(models.MovimientoVigencia.id_movimiento == movimiento_id).first()

def get_movimientos_vigencia(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.MovimientoVigencia).offset(skip).limit(limit).all()

def get_movimientos_by_cliente(db: Session, cliente_id: UUID):
    return db.query(models.MovimientoVigencia).filter(models.MovimientoVigencia.cliente_id == cliente_id).all()

def update_movimiento_vigencia(db: Session, movimiento_id: int, movimiento: schemas.MovimientoVigenciaCreate):
    try:
        db_movimiento = db.query(models.MovimientoVigencia).filter(models.MovimientoVigencia.id_movimiento == movimiento_id).first()
        if db_movimiento:
            movimiento_data = movimiento.model_dump()
            for key, value in movimiento_data.items():
                setattr(db_movimiento, key, value)
            db.commit()
            db.refresh(db_movimiento)
        return db_movimiento
    except Exception as e:
        db.rollback()
        raise e

def delete_movimiento_vigencia(db: Session, movimiento_id: int):
    try:
        db_movimiento = db.query(models.MovimientoVigencia).filter(models.MovimientoVigencia.id_movimiento == movimiento_id).first()
        if db_movimiento:
            db.delete(db_movimiento)
            db.commit()
            return True
        return False
    except Exception as e:
        db.rollback()
        raise e