"""
Ventana principal de la aplicación.
"""
from PyQt6.QtWidgets import QMainWindow
from ..cliente_api import ClienteAPI
from ..ui.main_window import MainWindow

class VentanaPrincipal(MainWindow):
    def __init__(self, cliente_api: ClienteAPI):
        super().__init__(cliente_api=cliente_api)
        # No necesitamos asignar self.cliente_api aquí ya que se hace en MainWindow
        # Aquí podemos agregar cualquier inicialización adicional si es necesaria
