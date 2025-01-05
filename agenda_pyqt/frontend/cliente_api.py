"""
Cliente para comunicarse con la API del backend.
"""
import requests
from typing import Optional, Dict, Any
from urllib.parse import urljoin
import logging

logger = logging.getLogger(__name__)

class ClienteAPI:
    def __init__(self):
        self.base_url = "http://localhost:8000"  # URL base sin el prefijo de la API
        self.token: Optional[str] = None
        
    def establecer_token(self, token: str):
        """Establece el token de autenticación"""
        self.token = token
        
    def obtener_headers(self, content_type: str = "application/json") -> Dict[str, str]:
        """Obtiene los headers con el token de autenticación"""
        headers = {"Content-Type": content_type}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def iniciar_sesion(self, email: str, password: str) -> Dict[str, Any]:
        """
        Inicia sesión en el sistema.
        
        Args:
            email: Correo electrónico del usuario
            password: Contraseña del usuario
            
        Returns:
            Dict con el token de acceso y su tipo
        """
        try:
            datos_login = {
                "username": email,  # El backend espera 'username' aunque sea un email
                "password": password
            }
            response = requests.post(
                f"{self.base_url}/api/v1/iniciar-sesion/token",
                data=datos_login,  # Usar data en lugar de json para form-data
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            response.raise_for_status()
            token_data = response.json()
            self.establecer_token(token_data["access_token"])
            return token_data
        except Exception as e:
            logger.error(f"Error en iniciar_sesion: {str(e)}")
            raise

    def verificar_primera_ejecucion(self) -> bool:
        """
        Verifica si es la primera ejecución del sistema.
        
        Returns:
            True si es la primera ejecución, False en caso contrario
        """
        try:
            url = f"{self.base_url}/api/v1/usuarios/verificar-primera-ejecucion"
            response = requests.get(
                url,
                headers=self.obtener_headers()
            )
            response.raise_for_status()
            return response.json().get("primera_ejecucion", False)
        except Exception as e:
            logger.error(f"Error en verificar_primera_ejecucion: {str(e)}")
            raise
    
    def obtener_clientes(self):
        """Obtiene la lista de clientes"""
        try:
            url = urljoin(self.base_url, "/api/v1/clientes/")
            headers = self.obtener_headers()
            logger.debug(f"Obteniendo clientes de URL: {url}")
            logger.debug(f"Headers: {headers}")
            
            response = requests.get(url, headers=headers)
            logger.debug(f"Código de respuesta: {response.status_code}")
            logger.debug(f"Respuesta: {response.text}")
            
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error en obtener_clientes: {str(e)}")
            raise
    
    def crear_cliente(self, datos_cliente):
        """Crea un nuevo cliente"""
        try:
            response = requests.post(
                urljoin(self.base_url, "/api/v1/clientes/"),
                headers=self.obtener_headers(),
                json=datos_cliente
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error en crear_cliente: {str(e)}")
            raise
    
    def obtener_movimientos_cliente(self, cliente_id: int):
        """Obtiene los movimientos de un cliente"""
        try:
            response = requests.get(
                urljoin(self.base_url, f"/api/v1/clientes/{cliente_id}/movimientos/"),
                headers=self.obtener_headers()
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error en obtener_movimientos_cliente: {str(e)}")
            raise
    
    def actualizar_cliente(self, cliente_id: int, datos_cliente):
        """Actualiza un cliente existente"""
        try:
            response = requests.put(
                urljoin(self.base_url, f"/api/v1/clientes/{cliente_id}/"),
                headers=self.obtener_headers(),
                json=datos_cliente
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error en actualizar_cliente: {str(e)}")
            raise
    
    def eliminar_cliente(self, cliente_id: int):
        """Elimina un cliente"""
        try:
            response = requests.delete(
                urljoin(self.base_url, f"/api/v1/clientes/{cliente_id}/"),
                headers=self.obtener_headers()
            )
            response.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"Error en eliminar_cliente: {str(e)}")
            raise
    
    def crear_movimiento(self, cliente_id: int, datos_movimiento):
        """Crea un nuevo movimiento para un cliente"""
        try:
            response = requests.post(
                urljoin(self.base_url, f"/api/v1/clientes/{cliente_id}/movimientos/"),
                headers=self.obtener_headers(),
                json=datos_movimiento
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error en crear_movimiento: {str(e)}")
            raise
    
    def actualizar_movimiento(self, movimiento_id: int, datos_movimiento):
        """Actualiza un movimiento existente"""
        try:
            response = requests.put(
                urljoin(self.base_url, f"/api/v1/movimientos/{movimiento_id}/"),
                headers=self.obtener_headers(),
                json=datos_movimiento
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error en actualizar_movimiento: {str(e)}")
            raise
    
    def eliminar_movimiento(self, movimiento_id: int):
        """Elimina un movimiento"""
        try:
            response = requests.delete(
                urljoin(self.base_url, f"/api/v1/movimientos/{movimiento_id}/"),
                headers=self.obtener_headers()
            )
            response.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"Error en eliminar_movimiento: {str(e)}")
            raise
