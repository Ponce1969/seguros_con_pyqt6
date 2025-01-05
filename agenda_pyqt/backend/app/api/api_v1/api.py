"""
Configuración principal de la API v1.
"""
from fastapi import APIRouter
from .endpoints import usuarios, iniciar_sesion

api_router = APIRouter()
api_router.include_router(iniciar_sesion.router, tags=["autenticacion"])
api_router.include_router(usuarios.router, prefix="/usuarios", tags=["usuarios"])
