# Proyecto Aseguradora Qt

Este proyecto es una aplicación de gestión de seguros que utiliza FastAPI para el backend y PyQt6 para el frontend. La base de datos utilizada es PostgreSQL y se gestiona mediante SQLAlchemy y Alembic.

## Requisitos

- Python 3.9 o superior
- Docker y Docker Compose

## Instalación

### Clonar el repositorio

```bash
git clone https://github.com/tu_usuario/aseguradora_qt.git
cd aseguradora_qt


python -m venv .segur
source .segur/bin/activate  # En Windows: .segur\Scripts\activate

pip install -r requirements.txt


Crea un archivo .env con las variables de entorno 

POSTGRES_PASSWORD=xxxxx
POSTGRES_USER=xxxxx
POSTGRES_DB=xxxxxx
POSTGRES_HOST=xxxxxx
POSTGRES_PORT=xxxxx
DB_URI=xxxxxx

ejecuta la aplicacion con Docker 

docker-compose up --build

Backend se ejecuta en 
http://localhost:8000. Puedes acceder a la documentación interactiva de la API en http://localhost:8000/docs.

Frontend
python frontend/main.py

estructura del proyecto:

C:\Users\gompa\Documents\Aseguradora_Qt\agenda_pyqt
│
├── .segur
│   └── (entorno virtual)
│
├── backend
│   ├── app
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── crud.py
│   │   ├── database.py
│   │   └── routers
│   │       └── __init__.py
│   ├── tests
│   │   └── test_main.py
│   └── Dockerfile
│
├── frontend
│   ├── __init__.py
│   ├── main.py
│   ├── ui
│   │   ├── __init__.py
│   │   ├── main_window.ui
│   │   ├── main_window.py
│   │   └── (otros archivos .ui y .py)
│   └── resources
│       ├── __init__.py
│       ├── images
│       │   └── (imágenes)
│       ├── icons
│       │   └── (iconos)
│       └── styles.qss
│
├── .env
├── docker-compose.yml
└── [README.md](http://_vscodecontentref_/3)