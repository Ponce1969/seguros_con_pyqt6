"""
Ventana de primera ejecución del sistema.
"""
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLineEdit, 
    QPushButton, QLabel, QMessageBox
)
from PyQt6.QtCore import Qt
import logging

from ..cliente_api import ClienteAPI

logger = logging.getLogger(__name__)

class VentanaPrimeraEjecucion(QMainWindow):
    def __init__(self, cliente_api: ClienteAPI):
        super().__init__()
        self.cliente_api = cliente_api
        self.setup_ui()
        
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        self.setWindowTitle("Configuración Inicial")
        self.setFixedSize(400, 300)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Título
        titulo = QLabel("Configuración Inicial del Sistema")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titulo)
        
        # Descripción
        descripcion = QLabel(
            "Este es el primer inicio del sistema. "
            "Por favor, configure el usuario administrador."
        )
        descripcion.setWordWrap(True)
        descripcion.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(descripcion)
        
        # Campos de entrada
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Correo electrónico")
        layout.addWidget(self.email_input)
        
        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Nombre")
        layout.addWidget(self.nombre_input)
        
        self.apellido_input = QLineEdit()
        self.apellido_input.setPlaceholderText("Apellido")
        layout.addWidget(self.apellido_input)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)
        
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirmar contraseña")
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.confirm_password_input)
        
        # Botón de crear
        crear_button = QPushButton("Crear Administrador")
        crear_button.clicked.connect(self.manejar_crear_admin)
        layout.addWidget(crear_button)
        
        # Estilo y espaciado
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)
        
    def manejar_crear_admin(self):
        """Maneja la creación del administrador"""
        # Validar campos
        email = self.email_input.text().strip()
        nombre = self.nombre_input.text().strip()
        apellido = self.apellido_input.text().strip()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()
        
        if not all([email, nombre, apellido, password, confirm_password]):
            QMessageBox.warning(
                self,
                "Error",
                "Por favor, complete todos los campos"
            )
            return
            
        if password != confirm_password:
            QMessageBox.warning(
                self,
                "Error",
                "Las contraseñas no coinciden"
            )
            return
            
        try:
            # TODO: Implementar la creación del primer administrador
            # cuando tengamos el endpoint correspondiente
            QMessageBox.information(
                self,
                "Éxito",
                "Administrador creado correctamente"
            )
            self.close()
            
        except Exception as e:
            logger.error(f"Error al crear administrador: {str(e)}")
            QMessageBox.critical(
                self,
                "Error",
                f"Error al crear el administrador: {str(e)}"
            )
