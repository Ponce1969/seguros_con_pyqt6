"""
Módulo principal del frontend de la aplicación de seguros.
"""
import logging

# Configurar logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

from .main_app import main

__version__ = "1.0.0"
__author__ = "Gonzalo Ponce"

__all__ = ['main']