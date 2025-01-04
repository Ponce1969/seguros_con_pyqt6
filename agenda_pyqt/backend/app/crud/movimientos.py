from sqlalchemy.orm import Session
from uuid import UUID
from ..models.movimiento import MovimientoVigencia
from ..schemas.movimiento import MovimientoVigenciaCreate

def create_movimiento_vigencia(db: Session, movimiento: MovimientoVigenciaCreate):
    """Crear un nuevo movimiento de vigencia"""
    try:
        movimiento_data = movimiento.model_dump()
        db_movimiento = MovimientoVigencia(**movimiento_data)
        db.add(db_movimiento)
        db.commit()
        db.refresh(db_movimiento)
        return db_movimiento
    except Exception as e:
        db.rollback()
        raise e

def get_movimiento_vigencia(db: Session, movimiento_id: int):
    """Obtener un movimiento de vigencia por ID"""
    return db.query(MovimientoVigencia).filter(MovimientoVigencia.id == movimiento_id).first()

def get_movimientos_vigencia(db: Session, skip: int = 0, limit: int = 100):
    """Obtener lista de movimientos de vigencia"""
    return db.query(MovimientoVigencia).offset(skip).limit(limit).all()

def get_movimientos_by_cliente(db: Session, cliente_id: UUID):
    """Obtener movimientos de vigencia por cliente"""
    return db.query(MovimientoVigencia).filter(MovimientoVigencia.cliente_id == cliente_id).all()

def update_movimiento_vigencia(db: Session, movimiento_id: int, movimiento: MovimientoVigenciaCreate):
    """Actualizar un movimiento de vigencia"""
    try:
        db_movimiento = db.query(MovimientoVigencia).filter(MovimientoVigencia.id == movimiento_id).first()
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
    """Eliminar un movimiento de vigencia"""
    try:
        db_movimiento = db.query(MovimientoVigencia).filter(MovimientoVigencia.id == movimiento_id).first()
        if db_movimiento:
            db.delete(db_movimiento)
            db.commit()
            return True
        return False
    except Exception as e:
        db.rollback()
        raise e
