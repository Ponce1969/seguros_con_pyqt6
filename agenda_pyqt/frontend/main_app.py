from PyQt6.QtWidgets import QApplication, QMessageBox
from .login_window import LoginWindow
from .main_window import MainWindow
import sys
import logging
import requests

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class AplicacionSeguros(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.token = None
        self.ventana_actual = None
        self.mostrar_login()
    
    def mostrar_login(self):
        """Muestra la ventana de inicio de sesión"""
        if self.ventana_actual:
            self.ventana_actual.close()
        
        self.ventana_actual = LoginWindow()
        self.ventana_actual.app = self  # Establecer referencia a la aplicación
        self.ventana_actual.show()
    
    def mostrar_ventana_principal(self):
        """Muestra la ventana principal"""
        if self.ventana_actual:
            self.ventana_actual.close()
        
        self.ventana_actual = MainWindow(self.token)
        self.ventana_actual.show()
    
    def set_auth_token(self, token: str):
        """Establece el token de autenticación y muestra la ventana principal"""
        logger.debug("Estableciendo token de autenticación")
        self.token = token
        self.mostrar_ventana_principal()
    
    def cerrar_sesion(self):
        """Cierra la sesión actual y vuelve a la ventana de login"""
        logger.debug("Cerrando sesión")
        self.token = None
        self.mostrar_login()
    
    def mostrar_error_y_salir(self, mensaje: str):
        """Muestra un mensaje de error y cierra la aplicación"""
        QMessageBox.critical(None, "Error", mensaje)
        sys.exit(1)

def main():
    try:
        app = AplicacionSeguros(sys.argv)
        return app.exec()
    except Exception as e:
        logger.error(f"Error crítico en la aplicación: {str(e)}")
        QMessageBox.critical(None, "Error", f"Error crítico en la aplicación: {str(e)}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
