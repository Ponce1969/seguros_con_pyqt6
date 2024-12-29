# Sistema de Gestión de Seguros con PyQt6

Sistema de gestión para una aseguradora desarrollado con PyQt6 y FastAPI.

## Características

- Frontend desarrollado con PyQt6
- Backend API REST con FastAPI
- Base de datos PostgreSQL
- Autenticación JWT
- Gestión de clientes y pólizas
- Sistema de roles y permisos
- Docker para desarrollo y despliegue

## Estructura del Proyecto

```
agenda_pyqt/
├── backend/           # Servidor FastAPI
│   ├── app/          # Código principal del backend
│   └── alembic/      # Migraciones de base de datos
├── frontend/         # Aplicación PyQt6
└── init-scripts/     # Scripts de inicialización de BD
```

## Requisitos

- Python 3.9+
- Docker y Docker Compose
- PostgreSQL 13+

## Configuración

1. Clonar el repositorio
2. Copiar `.env.example` a `.env` y configurar las variables
3. Ejecutar `docker-compose up --build`

## Desarrollo

El proyecto usa:
- FastAPI para el backend
- SQLAlchemy como ORM
- Alembic para migraciones
- PyQt6 para la interfaz de usuario
- JWT para autenticación
