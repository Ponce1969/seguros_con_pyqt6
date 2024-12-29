import os
from sqlalchemy import create_engine
from app.models import User, Base

DATABASE_URL = os.getenv('DATABASE_URL', "postgresql://Ponce1969:Gallinal2218@localhost:5433/seguros")

# Crear el engine
engine = create_engine(DATABASE_URL)

# Crear una sesión
from sqlalchemy.orm import sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# Consultar usuarios
users = db.query(User).all()
print("\nUsuarios en la base de datos:")
print("-" * 50)
for user in users:
    print(f"ID: {user.id}")
    print(f"Email: {user.email}")
    print(f"Role: {user.role}")
    print(f"Is Active: {user.is_active}")
    print("-" * 50)

print(f"\nTotal de usuarios: {len(users)}")
