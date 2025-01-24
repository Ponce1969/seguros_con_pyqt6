from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QTabWidget,
                            QSizePolicy, QMessageBox, QApplication)
from PyQt6.QtCore import Qt
import logging
from .views.components.tabs.corredores_tab import CorredoresTab
from .views.components.tabs.clientes_tab import ClientesTab
from .views.components.tabs.movimientos_tab import MovimientosTab

logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    def __init__(self, token):
        super().__init__()
        self.token = token
        self.setup_ui()
        
    def setup_ui(self):
        """Configura la interfaz de usuario principal"""
        self.setWindowTitle("Sistema de Seguros")
        
        # Configurar tamaño inicial y política de redimensionamiento
        self.resize(1200, 700)
        self.setMinimumSize(1000, 600)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Crear el widget de pestañas
        self.tab_widget = QTabWidget()
        
        # Pestaña de Clientes
        self.clientes_tab = ClientesTab(self.token)
        self.tab_widget.addTab(self.clientes_tab, "Clientes")
        
        # Pestaña de Movimientos
        self.movimientos_tab = MovimientosTab(self.token)
        self.tab_widget.addTab(self.movimientos_tab, "Movimientos")
        
        # Pestaña de Corredores
        self.corredores_tab = CorredoresTab(self.token)
        self.tab_widget.addTab(self.corredores_tab, "Corredores")
        
        layout.addWidget(self.tab_widget)
        
        # Centrar la ventana
        self.center_window()
        
    def center_window(self):
        """Centra la ventana en la pantalla"""
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        
        window_geometry = self.frameGeometry()
        center_point = screen_geometry.center()
        
        window_geometry.moveCenter(center_point)
        self.move(window_geometry.topLeft())
