from typing import List
from uuid import UUID
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import engine, SessionLocal
from . import models, schemas
from .routers import clientes, movimientos, corredores, tipos_seguros, users
import logging

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Crear las tablas
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir los routers
app.include_router(users.router)
app.include_router(clientes.router, prefix="/clients", tags=["clients"])
app.include_router(movimientos.router, prefix="/movements", tags=["movements"])
app.include_router(corredores.router, prefix="/corredores", tags=["corredores"])
app.include_router(tipos_seguros.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crear un cliente
@app.post("/clients/", response_model=schemas.Cliente, status_code=201)
def create_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    try:
        logger.debug(f"Datos recibidos: {cliente.model_dump()}")
        db_cliente = models.Cliente(**cliente.dict())
        db.add(db_cliente)
        db.commit()
        db.refresh(db_cliente)
        logger.debug(f"Cliente creado: {db_cliente.id}")
        return db_cliente
    except Exception as e:
        logger.error(f"Error al crear cliente: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error al crear el cliente: {str(e)}")

# Obtener todos los clientes
@app.get("/clients/", response_model=List[schemas.Cliente])
def read_clientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        clientes = db.query(models.Cliente).offset(skip).limit(limit).all()
        logger.debug(f"Clientes obtenidos: {len(clientes)}")
        return clientes
    except Exception as e:
        logger.error(f"Error al obtener clientes: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error al obtener los clientes: {str(e)}")

# Obtener un cliente por ID
@app.get("/clients/{cliente_id}", response_model=schemas.Cliente)
def read_cliente(cliente_id: UUID, db: Session = Depends(get_db)):
    try:
        cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
        if cliente is None:
            logger.error(f"Cliente no encontrado: {cliente_id}")
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        logger.debug(f"Cliente obtenido: {cliente.id}")
        return cliente
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

# Actualizar un cliente
@app.put("/clients/{cliente_id}", response_model=schemas.Cliente)
def update_cliente(cliente_id: UUID, cliente_actualizado: schemas.ClienteUpdate, db: Session = Depends(get_db)):
    try:
        logger.debug(f"Datos recibidos: {cliente_actualizado.model_dump()}")
        cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
        if cliente is None:
            logger.error(f"Cliente no encontrado: {cliente_id}")
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        for key, value in cliente_actualizado.dict(exclude_unset=True).items():
            setattr(cliente, key, value)
        db.commit()
        db.refresh(cliente)
        logger.debug(f"Cliente actualizado: {cliente.id}")
        return cliente
    except Exception as e:
        logger.error(f"Error al actualizar cliente: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error al actualizar el cliente: {str(e)}")

# Eliminar un cliente
@app.delete("/clients/{cliente_id}")
def delete_cliente(cliente_id: UUID, db: Session = Depends(get_db)):
    try:
        cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
        if cliente is None:
            logger.error(f"Cliente no encontrado: {cliente_id}")
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        db.delete(cliente)
        db.commit()
        logger.debug(f"Cliente eliminado: {cliente_id}")
        return {"message": "Cliente eliminado"}
    except Exception as e:
        logger.error(f"Error al eliminar cliente: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error al eliminar el cliente: {str(e)}")

# Endpoints para MovimientoVigencia
@app.post("/movements/", response_model=schemas.MovimientoVigencia)
def create_movimiento(movimiento: schemas.MovimientoVigenciaCreate, db: Session = Depends(get_db)):
    try:
        logger.debug(f"Datos recibidos: {movimiento.model_dump()}")
        
        # Verificar que el cliente existe
        cliente = crud.get_cliente(db, cliente_id=movimiento.cliente_id)
        if not cliente:
            logger.error(f"Cliente no encontrado: {movimiento.cliente_id}")
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        
        # Crear el movimiento
        try:
            nuevo_movimiento = crud.create_movimiento_vigencia(db=db, movimiento=movimiento)
            logger.debug(f"Movimiento creado: {nuevo_movimiento.id_movimiento}")
            return nuevo_movimiento
        except Exception as e:
            logger.error(f"Error al crear movimiento: {str(e)}")
            logger.error(traceback.format_exc())
            raise HTTPException(status_code=500, detail=f"Error al crear el movimiento: {str(e)}")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

@app.get("/movements/", response_model=List[schemas.MovimientoVigencia])
def read_movimientos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        movimientos = crud.get_movimientos_vigencia(db, skip=skip, limit=limit)
        logger.debug(f"Movimientos obtenidos: {len(movimientos)}")
        return movimientos
    except Exception as e:
        logger.error(f"Error al obtener movimientos: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error al obtener los movimientos: {str(e)}")

@app.get("/movements/{movimiento_id}", response_model=schemas.MovimientoVigencia)
def read_movimiento(movimiento_id: int, db: Session = Depends(get_db)):
    try:
        db_movimiento = crud.get_movimiento_vigencia(db, movimiento_id=movimiento_id)
        if db_movimiento is None:
            logger.error(f"Movimiento no encontrado: {movimiento_id}")
            raise HTTPException(status_code=404, detail="Movimiento no encontrado")
        logger.debug(f"Movimiento obtenido: {movimiento_id}")
        return db_movimiento
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

@app.get("/clients/{cliente_id}/movements/", response_model=List[schemas.MovimientoVigencia])
def read_movimientos_by_cliente(cliente_id: UUID, db: Session = Depends(get_db)):
    try:
        # Verificar que el cliente existe
        cliente = crud.get_cliente(db, cliente_id=cliente_id)
        if not cliente:
            logger.error(f"Cliente no encontrado: {cliente_id}")
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        movimientos = crud.get_movimientos_by_cliente(db, cliente_id=cliente_id)
        logger.debug(f"Movimientos obtenidos: {len(movimientos)}")
        return movimientos
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

@app.put("/movements/{movimiento_id}", response_model=schemas.MovimientoVigencia)
def update_movimiento(movimiento_id: int, movimiento: schemas.MovimientoVigenciaCreate, db: Session = Depends(get_db)):
    try:
        logger.debug(f"Datos recibidos: {movimiento.model_dump()}")
        db_movimiento = crud.update_movimiento_vigencia(db, movimiento_id=movimiento_id, movimiento=movimiento)
        if db_movimiento is None:
            logger.error(f"Movimiento no encontrado: {movimiento_id}")
            raise HTTPException(status_code=404, detail="Movimiento no encontrado")
        logger.debug(f"Movimiento actualizado: {movimiento_id}")
        return db_movimiento
    except Exception as e:
        logger.error(f"Error al actualizar movimiento: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error al actualizar el movimiento: {str(e)}")

@app.delete("/movements/{movimiento_id}")
def delete_movimiento(movimiento_id: int, db: Session = Depends(get_db)):
    try:
        success = crud.delete_movimiento_vigencia(db, movimiento_id=movimiento_id)
        if not success:
            logger.error(f"Movimiento no encontrado: {movimiento_id}")
            raise HTTPException(status_code=404, detail="Movimiento no encontrado")
        logger.debug(f"Movimiento eliminado: {movimiento_id}")
        return {"message": "Movimiento eliminado exitosamente"}
    except Exception as e:
        logger.error(f"Error al eliminar movimiento: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error al eliminar el movimiento: {str(e)}")