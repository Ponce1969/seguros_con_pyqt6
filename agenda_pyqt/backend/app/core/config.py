from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Aseguradora API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Configuración de la base de datos
    POSTGRES_SERVER: str = "postgres"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "aseguradora"
    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    # Configuración de seguridad
    SECRET_KEY: str = "tu_clave_secreta_super_segura_cambiar_en_produccion"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        case_sensitive = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.SQLALCHEMY_DATABASE_URI:
            self.SQLALCHEMY_DATABASE_URI = (
                f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
                f"{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"
            )

settings = Settings()
