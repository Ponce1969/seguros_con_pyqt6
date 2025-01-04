from sqlalchemy.orm import Session
from uuid import UUID
from ..models.cliente import Cliente
from ..schemas.cliente import ClienteCreate, ClienteUpdate

def get_cliente(db: Session, cliente_id: UUID):
    """Obtener un cliente por ID"""
    return db.query(Cliente).filter(Cliente.id == cliente_id).first()

def get_cliente_by_documento(db: Session, documento: str):
    """Obtener un cliente por documento"""
    return db.query(Cliente).filter(Cliente.numero_documento == documento).first()

def get_clientes(db: Session, skip: int = 0, limit: int = 100):
    """Obtener lista de clientes"""
    return db.query(Cliente).offset(skip).limit(limit).all()

def create_cliente(db: Session, cliente: ClienteCreate):
    """Crear un nuevo cliente"""
    db_cliente = Cliente(**cliente.dict())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

def update_cliente(db: Session, cliente_id: UUID, cliente: ClienteUpdate):
    """Actualizar un cliente existente"""
    db_cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if db_cliente:
        for key, value in cliente.dict(exclude_unset=True).items():
            setattr(db_cliente, key, value)
        db.commit()
        db.refresh(db_cliente)
    return db_cliente

def delete_cliente(db: Session, cliente_id: UUID):
    """Eliminar un cliente"""
    db_cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if db_cliente:
        db.delete(db_cliente)
        db.commit()
    return db_cliente
