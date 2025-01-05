from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db.base import Base
from .db.session import engine, SessionLocal
from .api.api_v1.api import api_router
from .core.config import settings
from .db.init_db import init_db
from .routers import clientes, movimientos
import logging

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Crear las tablas
Base.metadata.create_all(bind=engine)

# Inicializar la base de datos
db = SessionLocal()
try:
    init_db(db)
finally:
    db.close()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir el router principal de la API v1
app.include_router(api_router, prefix=settings.API_V1_STR)

# Incluir routers adicionales
app.include_router(clientes.router, prefix=f"{settings.API_V1_STR}/clientes", tags=["clientes"])
app.include_router(movimientos.router, prefix=f"{settings.API_V1_STR}/movimientos", tags=["movimientos"])

@app.get("/")
def read_root():
    return {
        "app": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "running"
    }