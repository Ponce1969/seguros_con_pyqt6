"""
Importa todos los modelos para que Alembic pueda detectar las migraciones.
"""
from .base_class import Base  # noqa
from ..models.usuario import Usuario  # noqa
from ..models.cliente import Cliente  # noqa
from ..models.corredor import Corredor  # noqa
from ..models.tipo_seguro import TipoSeguro  # noqa
from ..models.movimiento import MovimientoVigencia  # noqa
