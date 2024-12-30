"""
Base schemas y utilidades comunes para validación.
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re

# Definición de expresiones regulares para validar formatos
PHONE_REGEX = r'^[0-9+\-\s()\/]*$'  # Más flexible: permite números, +, -, /, espacios y paréntesis
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

def validate_phone(value: Optional[str]) -> Optional[str]:
    """Valida el formato de un número telefónico."""
    if not value:
        return value
    if not re.match(PHONE_REGEX, value):
        raise ValueError('Formato de teléfono inválido')
    return value

def validate_email(value: Optional[str]) -> Optional[str]:
    """Valida y normaliza un correo electrónico."""
    if not value:
        return value
    if not re.match(EMAIL_REGEX, value.lower()):
        raise ValueError('Formato de email inválido')
    return value.lower()
