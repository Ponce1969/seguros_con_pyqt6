from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
import logging
import traceback
from sqlalchemy import or_

from ..db.session import SessionLocal
from ..models.cliente import Cliente
from ..models.usuario import Usuario
from ..schemas import cliente as schemas
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

@router.post("/", response_model=schemas.Cliente, status_code=201)
def create_cliente(
    cliente: schemas.ClienteCreate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    try:
        logger.debug(f"Datos recibidos: {cliente.model_dump()}")
        logger.debug(f"Usuario actual: {current_user.email} (ID: {current_user.id})")
        
        # Crear el cliente con los IDs del usuario actual
        db_cliente = Cliente(
            **cliente.dict(),
            creado_por_id=current_user.id,
            modificado_por_id=current_user.id
        )
        db.add(db_cliente)
        db.commit()
        db.refresh(db_cliente)
        logger.debug(f"Cliente creado: {db_cliente.id}")
        return db_cliente
    except Exception as e:
        logger.error(f"Error al crear cliente: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error al crear el cliente: {str(e)}")

@router.get("/", response_model=List[schemas.Cliente])
def read_clientes(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Obtiene la lista de clientes.
    """
    try:
        logger.debug(f"Obteniendo clientes. Usuario: {current_user.email} (ID: {current_user.id})")
        clientes = db.query(Cliente).offset(skip).limit(limit).all()
        logger.debug(f"Clientes encontrados: {len(clientes)}")
        
        # Transformar los clientes al formato del schema
        return [
            schemas.Cliente(
                id=cliente.id,
                numero_cliente=cliente.numero_cliente,
                nombres=cliente.nombres,
                apellidos=cliente.apellidos,
                tipo_documento=cliente.tipo_documento,
                numero_documento=cliente.numero_documento,
                fecha_nacimiento=cliente.fecha_nacimiento,
                direccion=cliente.direccion,
                localidad=cliente.localidad,
                telefonos=cliente.telefonos,
                movil=cliente.movil,
                mail=cliente.mail,
                corredor=cliente.corredor,
                observaciones=cliente.observaciones,
                creado_por_id=cliente.creado_por_id,
                modificado_por_id=cliente.modificado_por_id,
                fecha_creacion=cliente.fecha_creacion,
                fecha_modificacion=cliente.fecha_modificacion,
                movimientos_vigencias=[]  # Lista vacía por defecto
            )
            for cliente in clientes
        ]
    except Exception as e:
        logger.error(f"Error al obtener clientes: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error al obtener los clientes: {str(e)}")

@router.get("/por-corredor/{corredor_numero}", response_model=List[schemas.ClientePorCorredor])
def read_clientes_por_corredor(
    corredor_numero: int,
    skip: int = 0,
    limit: int = 10,
    search: str = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Obtiene la lista de clientes asociados a un corredor específico.
    Los clientes se ordenan por fecha de modificación descendente para mostrar los más recientes primero.
    
    Parámetros:
    - corredor_numero: Número del corredor
    - skip: Número de registros a saltar (para paginación)
    - limit: Número máximo de registros a devolver
    - search: Texto para buscar en nombres, apellidos, documento o email
    """
    try:
        logger.debug(f"Usuario {current_user.email} buscando clientes para el corredor: {corredor_numero}")
        logger.debug(f"Parámetros: skip={skip}, limit={limit}, search={search}")
        
        # Construir la query base
        query = db.query(Cliente).filter(Cliente.corredor == corredor_numero)
        
        # Agregar búsqueda si se especifica
        if search:
            search = f"%{search}%"
            query = query.filter(
                or_(
                    Cliente.nombres.ilike(search),
                    Cliente.apellidos.ilike(search),
                    Cliente.numero_documento.ilike(search),
                    Cliente.mail.ilike(search)
                )
            )
        
        # Log de la query SQL
        logger.debug(f"Query SQL: {query.statement}")
        
        # Ejecutar la query con orden y límites
        clientes = query.order_by(Cliente.fecha_modificacion.desc())\
            .offset(skip)\
            .limit(limit)\
            .all()
        
        # Obtener el total de registros para esta búsqueda
        total = query.count()
        
        if not clientes:
            logger.debug(f"No se encontraron clientes para el corredor {corredor_numero}")
            return []
            
        logger.debug(f"Se encontraron {len(clientes)} clientes para el corredor {corredor_numero}")
        logger.debug(f"Total de registros sin límite: {total}")
        
        return clientes
        
    except Exception as e:
        logger.error(f"Error al buscar clientes por corredor: {str(e)}")
        logger.error(f"Detalles del error: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Error al buscar clientes para el corredor {corredor_numero}: {str(e)}"
        )

@router.get("/{cliente_id}", response_model=schemas.Cliente)
def read_cliente(
    cliente_id: UUID, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    try:
        logger.debug(f"Buscando cliente {cliente_id}. Usuario: {current_user.email}")
        db_cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
        if db_cliente is None:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        return db_cliente
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al obtener cliente: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error al obtener el cliente: {str(e)}")

@router.put("/{cliente_id}", response_model=schemas.Cliente)
def update_cliente(
    cliente_id: UUID, 
    cliente_actualizado: schemas.ClienteUpdate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    try:
        logger.debug(f"Actualizando cliente {cliente_id}. Usuario: {current_user.email}")
        db_cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
        if not db_cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        
        # Actualizar los campos del cliente
        for field, value in cliente_actualizado.dict(exclude_unset=True).items():
            setattr(db_cliente, field, value)
        
        # Actualizar el ID del usuario que modificó
        db_cliente.modificado_por_id = current_user.id
        
        db.commit()
        db.refresh(db_cliente)
        logger.debug(f"Cliente actualizado: {db_cliente.id}")
        return db_cliente
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al actualizar cliente: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error al actualizar el cliente: {str(e)}")

@router.delete("/{cliente_id}")
def delete_cliente(
    cliente_id: UUID, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    try:
        logger.debug(f"Eliminando cliente {cliente_id}. Usuario: {current_user.email}")
        db_cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
        if not db_cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        
        db.delete(db_cliente)
        db.commit()
        logger.debug(f"Cliente eliminado: {cliente_id}")
        return {"message": "Cliente eliminado exitosamente"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al eliminar cliente: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error al eliminar el cliente: {str(e)}")
