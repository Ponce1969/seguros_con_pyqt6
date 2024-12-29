"""
Schemas relacionados con la entidad TipoSeguro.
"""
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class TipoSeguroBase(BaseModel):
    """Modelo base para tipos de seguro."""
    aseguradora: str = Field(description="Nombre de la aseguradora")
    codigo: str = Field(description="Código del tipo de seguro")
    descripcion: str = Field(description="Descripción del tipo de seguro")

    model_config = ConfigDict(from_attributes=True)

class TipoSeguroCreate(TipoSeguroBase):
    """Modelo para crear nuevos tipos de seguro."""
    id_tipo: int = Field(description="ID del tipo de seguro")

class TipoSeguroUpdate(BaseModel):
    """Modelo para actualizar tipos de seguro existentes."""
    aseguradora: Optional[str] = Field(None)
    codigo: Optional[str] = Field(None)
    descripcion: Optional[str] = Field(None)

    model_config = ConfigDict(from_attributes=True)

class TipoSeguro(TipoSeguroBase):
    """Modelo completo de tipo de seguro."""
    id_tipo: int = Field(description="ID del tipo de seguro")
