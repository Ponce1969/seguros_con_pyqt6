from .usuario import Usuario
from .cliente import Cliente
from .corredor import Corredor
from .tipo_seguro import TipoSeguro
from .movimiento import MovimientoVigencia
from ..db.base import Base

# Para mantener compatibilidad con código existente
User = Usuario

__all__ = [
    "User",
    "Cliente",
    "Corredor",
    "TipoSeguro",
    "MovimientoVigencia",
    "Base"
]
