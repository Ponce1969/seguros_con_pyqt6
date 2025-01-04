# Aseguradora API Backend

API REST para la gestión de una aseguradora, construida con FastAPI y PostgreSQL.

## Requisitos

- Python 3.9+
- Docker y Docker Compose
- PostgreSQL 13+

## Configuración

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd backend
```

2. Crear archivo de variables de entorno:
```bash
cp .env.example .env
# Editar .env con tus valores
```

3. Construir y levantar los contenedores:
```bash
docker-compose up --build -d
```

## Estructura del Proyecto

```
backend/
├── app/
│   ├── core/          # Configuración central y utilidades
│   ├── crud/          # Operaciones CRUD
│   ├── db/            # Configuración de base de datos
│   ├── models/        # Modelos SQLAlchemy
│   ├── routers/       # Endpoints de la API
│   └── schemas/       # Esquemas Pydantic
├── docker/           # Archivos Docker
└── tests/           # Tests
```

## Endpoints Principales

- `POST /api/v1/token` - Obtener token de acceso
- `GET /api/v1/clients/` - Listar clientes
- `POST /api/v1/clients/` - Crear cliente
- `GET /api/v1/clients/{id}` - Obtener cliente por ID
- `PUT /api/v1/clients/{id}` - Actualizar cliente
- `DELETE /api/v1/clients/{id}` - Eliminar cliente

## Desarrollo

1. Instalar dependencias de desarrollo:
```bash
pip install -r requirements.txt
```

2. Ejecutar tests:
```bash
pytest
```

## Producción

Para desplegar en producción:

1. Asegurarse de configurar variables de entorno seguras
2. Usar un servidor WSGI como Gunicorn
3. Configurar HTTPS
4. Implementar rate limiting
5. Configurar backups de la base de datos
