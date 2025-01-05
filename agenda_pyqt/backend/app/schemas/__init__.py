"""
Exporta todos los schemas para facilitar su importación.
"""

from .token import Token, TokenPayload
from .usuario import (
    Usuario,
    UsuarioBase,
    UsuarioCreate,
    UsuarioUpdate,
    # Alias para mantener compatibilidad
    User,
    UserBase,
    UserCreate,
    UserUpdate,
)
from .cliente import (
    Cliente,
    ClienteBase,
    ClienteCreate,
    ClienteUpdate,
)
from .movimiento import (
    MovimientoVigencia,
    MovimientoVigenciaBase,
    MovimientoVigenciaCreate,
    MovimientoVigenciaUpdate,
)
from .corredor import (
    Corredor,
    CorredorBase,
    CorredorCreate,
    CorredorUpdate,
)
from .tipo_seguro import (
    TipoSeguro,
    TipoSeguroBase,
    TipoSeguroCreate,
    TipoSeguroUpdate,
)

__all__ = [
    # Token schemas
    'Token', 'TokenPayload',
    # Cliente schemas
    'Cliente', 'ClienteCreate', 'ClienteUpdate', 'ClienteBase',
    # Usuario schemas
    'Usuario', 'UsuarioCreate', 'UsuarioUpdate', 'UsuarioBase',
    'User', 'UserCreate', 'UserUpdate', 'UserBase',
    # Corredor schemas
    'Corredor', 'CorredorCreate', 'CorredorUpdate', 'CorredorBase',
    # MovimientoVigencia schemas
    'MovimientoVigencia', 'MovimientoVigenciaCreate', 'MovimientoVigenciaUpdate', 'MovimientoVigenciaBase',
    # TipoSeguro schemas
    'TipoSeguro', 'TipoSeguroCreate', 'TipoSeguroUpdate', 'TipoSeguroBase',
]
