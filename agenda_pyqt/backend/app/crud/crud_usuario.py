"""
Operaciones CRUD para usuarios.
"""
from typing import Any, Dict, Optional, Union, List
from sqlalchemy.orm import Session

from ..core.security import get_password_hash, verify_password
from ..models.usuario import Usuario
from ..schemas.usuario import UsuarioCreate, UsuarioUpdate

class CRUDUsuario:
    def get(self, db: Session, id: int) -> Optional[Usuario]:
        """Obtener usuario por ID"""
        return db.query(Usuario).filter(Usuario.id == id).first()

    def get_by_email(self, db: Session, *, email: str) -> Optional[Usuario]:
        """Obtener usuario por email"""
        return db.query(Usuario).filter(Usuario.email == email).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Usuario]:
        """Obtener lista de usuarios"""
        return db.query(Usuario).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: UsuarioCreate) -> Usuario:
        """Crear nuevo usuario"""
        db_obj = Usuario(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            nombre=obj_in.nombre,
            apellido=obj_in.apellido,
            username=obj_in.username,
            is_superuser=obj_in.is_superuser,
            is_active=obj_in.is_active,
            role=obj_in.role,
            comision_porcentaje=obj_in.comision_porcentaje
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: Usuario,
        obj_in: Union[UsuarioUpdate, Dict[str, Any]]
    ) -> Usuario:
        """Actualizar usuario existente"""
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        
        if update_data.get("password"):
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        
        for field in update_data:
            setattr(db_obj, field, update_data[field])
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, id: int) -> Usuario:
        """Eliminar usuario"""
        obj = db.query(Usuario).get(id)
        db.delete(obj)
        db.commit()
        return obj

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[Usuario]:
        """Autenticar usuario"""
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: Usuario) -> bool:
        """Verificar si el usuario está activo"""
        return user.is_active

    def is_superuser(self, user: Usuario) -> bool:
        """Verificar si el usuario es superusuario"""
        return user.is_superuser

crud_usuario = CRUDUsuario()
