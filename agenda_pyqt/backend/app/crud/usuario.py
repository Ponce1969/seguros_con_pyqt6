"""
Operaciones CRUD para la entidad Usuario.
"""
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from passlib.context import CryptContext

from app.models.usuario import Usuario
from app.schemas.usuario import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UsuarioService:
    def get_password_hash(self, password: str) -> str:
        """Genera un hash de la contraseña."""
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verifica si la contraseña coincide con el hash."""
        return pwd_context.verify(plain_password, hashed_password)

    async def get_by_email(self, db: Session, email: str) -> Optional[Usuario]:
        """Obtiene un usuario por su email."""
        return await db.execute(
            select(Usuario).where(Usuario.email == email)
        ).scalar_one_or_none()

    async def get_by_username(self, db: Session, username: str) -> Optional[Usuario]:
        """Obtiene un usuario por su nombre de usuario."""
        return await db.execute(
            select(Usuario).where(Usuario.username == username)
        ).scalar_one_or_none()

    async def create(self, db: Session, *, obj_in: UserCreate) -> Usuario:
        """Crea un nuevo usuario."""
        db_obj = Usuario(
            email=obj_in.email,
            username=obj_in.username,
            hashed_password=self.get_password_hash(obj_in.password),
            is_superuser=obj_in.is_superuser,
            is_active=obj_in.is_active
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def create_superuser(self, db: Session, email: str, username: str, password: str) -> Usuario:
        """Crea un superusuario."""
        user = UserCreate(
            email=email,
            username=username,
            password=password,
            is_superuser=True,
            is_active=True
        )
        return await self.create(db, obj_in=user)

usuario_service = UsuarioService()
