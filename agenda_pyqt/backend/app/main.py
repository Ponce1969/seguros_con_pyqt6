from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db.base import Base
from .db.session import engine, SessionLocal
from .routers import clientes, movimientos, corredores, tipos_seguros, users, auth
from .core.config import settings
from .db.init_db import init_db
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
    version=settings.VERSION
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir los routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(users.router, prefix=settings.API_V1_STR)
app.include_router(clientes.router, prefix=f"{settings.API_V1_STR}/clients", tags=["clients"])
app.include_router(movimientos.router, prefix=f"{settings.API_V1_STR}/movements", tags=["movements"])
app.include_router(corredores.router, prefix=f"{settings.API_V1_STR}/corredores", tags=["corredores"])
app.include_router(tipos_seguros.router, prefix=f"{settings.API_V1_STR}/tipos-seguros", tags=["tipos_seguros"])

@app.get("/")
def read_root():
    return {
        "app": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "running"
    }