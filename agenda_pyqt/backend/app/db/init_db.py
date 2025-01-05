from sqlalchemy.orm import Session
from ..models.usuario import Usuario
from ..schemas.usuario import UsuarioCreate
from ..core.config import settings
from ..core.security import get_password_hash


def init_db(db: Session) -> None:
    """
    Inicializa la base de datos con un usuario administrador si no existe.
    """
    # Verificar si ya existe un usuario administrador
    user = db.query(Usuario).filter(Usuario.email == settings.FIRST_SUPERUSER).first()
    if not user:
        user_in = UsuarioCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            nombre="Admin",
            apellido="Sistema",
            username="admin",
            is_superuser=True,
            is_active=True,
            role="admin",
            comision_porcentaje=0.0
        )
        user = Usuario(
            email=user_in.email,
            nombre=user_in.nombre,
            apellido=user_in.apellido,
            username=user_in.username,
            hashed_password=get_password_hash(user_in.password),
            is_superuser=user_in.is_superuser,
            is_active=user_in.is_active,
            role=user_in.role,
            comision_porcentaje=user_in.comision_porcentaje
        )
        db.add(user)
        db.commit()
        db.refresh(user)
