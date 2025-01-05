from PyQt6.QtWidgets import QApplication, QMessageBox
from .ventanas.ventana_inicio_sesion import VentanaInicioSesion
from .ventanas.ventana_primera_ejecucion import VentanaPrimeraEjecucion
from .ventanas.ventana_principal import VentanaPrincipal
from .cliente_api import ClienteAPI
import sys
import logging

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class AplicacionSeguros(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.cliente_api = ClienteAPI()
        self.ventana_actual = None
        self.rol_usuario = None
        self.verificar_primera_ejecucion()
    
    def verificar_primera_ejecucion(self):
        """Verifica si es la primera ejecución del sistema"""
        try:
            logger.debug("Verificando estado inicial del sistema...")
            es_primera_ejecucion = self.cliente_api.verificar_primera_ejecucion()
            
            if es_primera_ejecucion:
                logger.debug("Primera ejecución detectada, mostrando ventana de configuración inicial")
                self.mostrar_ventana_primera_ejecucion()
            else:
                logger.debug("Sistema ya configurado, mostrando ventana de inicio de sesión")
                self.mostrar_ventana_inicio_sesion()
                
        except Exception as e:
            error_msg = f"Error al verificar el estado del sistema: {str(e)}"
            logger.error(error_msg)
            self.mostrar_error_y_salir(error_msg)
    
    def mostrar_ventana_primera_ejecucion(self):
        """Muestra la ventana de configuración inicial"""
        if self.ventana_actual:
            self.ventana_actual.close()
        self.ventana_actual = VentanaPrimeraEjecucion(self.cliente_api)
        self.ventana_actual.show()
    
    def mostrar_ventana_inicio_sesion(self):
        """Muestra la ventana de inicio de sesión"""
        if self.ventana_actual:
            self.ventana_actual.close()
        self.ventana_actual = VentanaInicioSesion(self.cliente_api)
        self.ventana_actual.inicio_sesion_exitoso.connect(self.manejar_inicio_sesion_exitoso)
        self.ventana_actual.show()
    
    def mostrar_ventana_principal(self):
        """Muestra la ventana principal"""
        if self.ventana_actual:
            self.ventana_actual.close()
        self.ventana_actual = VentanaPrincipal(self.cliente_api)
        self.ventana_actual.show()
    
    def manejar_inicio_sesion_exitoso(self, token_data: dict):
        """Maneja el inicio de sesión exitoso"""
        logger.debug("Inicio de sesión exitoso, mostrando ventana principal")
        self.mostrar_ventana_principal()
    
    def mostrar_error_y_salir(self, mensaje: str):
        """Muestra un mensaje de error y cierra la aplicación"""
        QMessageBox.critical(None, "Error", mensaje)
        sys.exit(1)

def main():
    app = AplicacionSeguros(sys.argv)
    sys.exit(app.exec())
