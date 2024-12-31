"""
Operaciones CRUD para la entidad Cliente.
"""
from typing import List, Optional, Union
from sqlalchemy.orm import Session
from sqlalchemy import select, or_
from sqlalchemy.exc import IntegrityError

from app.models.cliente import Cliente
from app.models.usuario import Usuario
from app.schemas.cliente import ClienteCreate, ClienteUpdate

class ClienteService:
    async def create(self, db: Session, *, cliente: ClienteCreate, user_id: int) -> Cliente:
        """Crear un nuevo cliente con número seguro."""
        try:
            db_cliente = Cliente(
                **cliente.model_dump(exclude={'numero_cliente'}),
                creado_por_id=user_id,
                modificado_por_id=user_id
            )
            
            db.add(db_cliente)
            await db.commit()
            await db.refresh(db_cliente)
            return db_cliente
            
        except IntegrityError:
            await db.rollback()
            raise ValueError("Error de integridad al crear el cliente")

    async def get_by_any_id(self, db: Session, identifier: Union[str, int], current_user: Usuario) -> Optional[Cliente]:
        """Buscar cliente por UUID o número de cliente."""
        try:
            query = select(Cliente)
            
            if isinstance(identifier, str) and len(identifier) == 36:
                query = query.where(Cliente.id == identifier)
            else:
                query = query.where(Cliente.numero_cliente == int(identifier))
            
            # Si no es superusuario, solo ver sus propios clientes
            if not current_user.is_superuser:
                query = query.where(Cliente.creado_por_id == current_user.id)
            
            return await db.execute(query).scalar_one_or_none()
        except (ValueError, TypeError):
            return None

    async def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        current_user: Usuario
    ) -> List[Cliente]:
        """Obtener múltiples clientes con búsqueda opcional."""
        query = select(Cliente)
        
        # Si no es superusuario, solo ver sus propios clientes
        if not current_user.is_superuser:
            query = query.where(Cliente.creado_por_id == current_user.id)
        
        if search:
            search_filter = or_(
                Cliente.nombres.ilike(f"%{search}%"),
                Cliente.apellidos.ilike(f"%{search}%"),
                Cliente.documentos.ilike(f"%{search}%"),
                Cliente.mail.ilike(f"%{search}%")
            )
            query = query.where(search_filter)
        
        return (await db.execute(
            query.offset(skip).limit(limit)
        )).scalars().all()

    async def update(
        self,
        db: Session,
        *,
        db_obj: Cliente,
        obj_in: ClienteUpdate,
        current_user: Usuario
    ) -> Cliente:
        """Actualizar cliente existente."""
        # Verificar permisos
        if not current_user.is_superuser and db_obj.creado_por_id != current_user.id:
            raise PermissionError("No tienes permiso para modificar este cliente")
            
        update_data = obj_in.model_dump(exclude_unset=True)
        update_data["modificado_por_id"] = current_user.id
        
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(
        self,
        db: Session,
        *,
        id: Union[str, int],
        current_user: Usuario
    ) -> Optional[Cliente]:
        """Eliminar cliente por ID."""
        obj = await self.get_by_any_id(db, id, current_user)
        if obj:
            # Verificar permisos
            if not current_user.is_superuser and obj.creado_por_id != current_user.id:
                raise PermissionError("No tienes permiso para eliminar este cliente")
                
            await db.delete(obj)
            await db.commit()
        return obj

cliente_service = ClienteService()
