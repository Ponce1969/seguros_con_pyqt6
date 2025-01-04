from sqlalchemy.orm import Session
from ..core.security import get_password_hash
from ..models.user import User
from ..core.config import settings

def init_db(db: Session) -> None:
    """Inicializa la base de datos con datos necesarios"""
    
    # Crear usuario admin si no existe
    admin_email = "admin@example.com"
    admin = db.query(User).filter(User.email == admin_email).first()
    if not admin:
        admin = User(
            name="Admin",
            email=admin_email,
            password=get_password_hash("admin"),
            is_active=True,
            role="admin"
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)
