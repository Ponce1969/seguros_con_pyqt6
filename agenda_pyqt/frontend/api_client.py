import requests
from typing import Optional

class APIClient:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.token: Optional[str] = None
        
    def set_token(self, token: str):
        """Establece el token de autenticación"""
        self.token = token
        
    def get_headers(self):
        """Obtiene los headers con el token de autenticación"""
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers
    
    def get_clientes(self):
        """Obtiene la lista de clientes"""
        response = requests.get(
            f"{self.base_url}/clientes/",
            headers=self.get_headers()
        )
        return response.json()
    
    def crear_cliente(self, cliente_data):
        """Crea un nuevo cliente"""
        response = requests.post(
            f"{self.base_url}/clientes/",
            headers=self.get_headers(),
            json=cliente_data
        )
        return response.json()
    
    # Más métodos para otras operaciones...
