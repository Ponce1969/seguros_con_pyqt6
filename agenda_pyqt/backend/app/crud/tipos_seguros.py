from sqlalchemy.orm import Session
from ..models.tipo_seguro import TipoSeguro
from ..schemas.tipo_seguro import TipoSeguroCreate, TipoSeguroUpdate

def get_tipo_seguro(db: Session, tipo_id: int):
    """Obtener un tipo de seguro por ID"""
    return db.query(TipoSeguro).filter(TipoSeguro.id == tipo_id).first()

def get_tipos_seguros(db: Session, skip: int = 0, limit: int = 100):
    """Obtener lista de tipos de seguro"""
    return db.query(TipoSeguro).offset(skip).limit(limit).all()

def create_tipo_seguro(db: Session, tipo: TipoSeguroCreate):
    """Crear un nuevo tipo de seguro"""
    db_tipo = TipoSeguro(**tipo.dict())
    db.add(db_tipo)
    db.commit()
    db.refresh(db_tipo)
    return db_tipo

def update_tipo_seguro(db: Session, tipo_id: int, tipo: TipoSeguroUpdate):
    """Actualizar un tipo de seguro existente"""
    db_tipo = get_tipo_seguro(db, tipo_id)
    if db_tipo:
        for key, value in tipo.dict(exclude_unset=True).items():
            setattr(db_tipo, key, value)
        db.commit()
        db.refresh(db_tipo)
    return db_tipo

def delete_tipo_seguro(db: Session, tipo_id: int):
    """Eliminar un tipo de seguro"""
    db_tipo = get_tipo_seguro(db, tipo_id)
    if db_tipo:
        db.delete(db_tipo)
        db.commit()
        return True
    return False
