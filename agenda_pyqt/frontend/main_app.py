from PyQt6.QtWidgets import QApplication, QMessageBox
from .login_window import LoginWindow
from .first_run_window import FirstRunWindow
from .api_client import APIClient
import sys
import requests
import logging

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class SegurosApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.api_client = APIClient()
        self.current_window = None
        self.user_role = None
        self.check_first_run()
    
    def check_first_run(self):
        """Verifica si es la primera ejecución del sistema"""
        try:
            logger.debug("Verificando estado inicial del sistema...")
            response = requests.get("http://localhost:8000/users/check-first-run")
            logger.debug(f"Respuesta del servidor: {response.status_code}")
            logger.debug(f"Contenido de la respuesta: {response.text}")
            
            if response.status_code == 200:
                data = response.json()
                if data.get("first_run", False):
                    logger.debug("Primera ejecución detectada, mostrando ventana de configuración inicial")
                    self.show_first_run_window()
                else:
                    logger.debug("Sistema ya configurado, mostrando ventana de login")
                    self.show_login_window()
            else:
                error_msg = f"Error al verificar el estado del sistema. Código: {response.status_code}, Respuesta: {response.text}"
                logger.error(error_msg)
                self.show_error_and_exit(error_msg)
        except requests.exceptions.ConnectionError as e:
            error_msg = "No se pudo conectar con el servidor. Asegúrate de que el backend esté funcionando."
            logger.error(f"{error_msg} Error: {str(e)}")
            self.show_error_and_exit(error_msg)
        except Exception as e:
            error_msg = f"Error inesperado al verificar el estado del sistema: {str(e)}"
            logger.error(error_msg)
            self.show_error_and_exit(error_msg)
    
    def show_first_run_window(self):
        """Muestra la ventana de configuración inicial"""
        if self.current_window:
            self.current_window.close()
        self.current_window = FirstRunWindow()
        self.current_window.app = self
        self.current_window.show()
    
    def show_login_window(self):
        """Muestra la ventana de login"""
        if self.current_window:
            self.current_window.close()
        self.current_window = LoginWindow()
        self.current_window.app = self
        self.current_window.show()
    
    def show_main_window(self, token=None):
        """Muestra la ventana principal de la aplicación"""
        if self.current_window:
            self.current_window.close()
        from .main_window import MainWindow
        self.current_window = MainWindow(token)
        self.current_window.show()
    
    def set_auth_token(self, token: str):
        """Establece el token de autenticación"""
        self.api_client.set_token(token)
        self.show_main_window(token)
    
    def set_user_role(self, role: str):
        """Establece el rol del usuario actual"""
        self.user_role = role
    
    def show_error_and_exit(self, message: str):
        """Muestra un error y cierra la aplicación"""
        QMessageBox.critical(None, "Error Fatal", message)
        sys.exit(1)

def main():
    app = SegurosApp(sys.argv)
    sys.exit(app.exec())
