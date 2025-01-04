from sqlalchemy.orm import Session
from ..models.corredor import Corredor
from ..schemas.corredor import CorredorCreate, CorredorUpdate

def get_corredor(db: Session, corredor_id: int):
    """Obtener un corredor por ID"""
    return db.query(Corredor).filter(Corredor.numero == corredor_id).first()

def get_corredores(db: Session, skip: int = 0, limit: int = 100):
    """Obtener lista de corredores"""
    return db.query(Corredor).offset(skip).limit(limit).all()

def create_corredor(db: Session, corredor: CorredorCreate):
    """Crear un nuevo corredor"""
    db_corredor = Corredor(**corredor.dict())
    db.add(db_corredor)
    db.commit()
    db.refresh(db_corredor)
    return db_corredor

def update_corredor(db: Session, corredor_id: int, corredor: CorredorUpdate):
    """Actualizar un corredor existente"""
    db_corredor = get_corredor(db, corredor_id)
    if db_corredor:
        for key, value in corredor.dict(exclude_unset=True).items():
            setattr(db_corredor, key, value)
        db.commit()
        db.refresh(db_corredor)
    return db_corredor

def delete_corredor(db: Session, corredor_id: int):
    """Eliminar un corredor"""
    db_corredor = get_corredor(db, corredor_id)
    if db_corredor:
        db.delete(db_corredor)
        db.commit()
        return True
    return False
