"""
Ventana de inicio de sesión.
"""
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLineEdit, 
    QPushButton, QLabel, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
import logging

from ..cliente_api import ClienteAPI

logger = logging.getLogger(__name__)

class VentanaInicioSesion(QMainWindow):
    # Señal que se emite cuando el inicio de sesión es exitoso
    inicio_sesion_exitoso = pyqtSignal(dict)
    
    def __init__(self, cliente_api: ClienteAPI):
        super().__init__()
        self.cliente_api = cliente_api
        self.setup_ui()
        
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        self.setWindowTitle("Iniciar Sesión")
        self.setFixedSize(400, 200)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Título
        titulo = QLabel("Iniciar Sesión")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titulo)
        
        # Campo de email
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Correo electrónico")
        layout.addWidget(self.email_input)
        
        # Campo de contraseña
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)
        
        # Botón de login
        login_button = QPushButton("Iniciar Sesión")
        login_button.clicked.connect(self.manejar_inicio_sesion)
        layout.addWidget(login_button)
        
        # Estilo y espaciado
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)
        
    def manejar_inicio_sesion(self):
        """Maneja el proceso de inicio de sesión"""
        email = self.email_input.text().strip()
        password = self.password_input.text()
        
        if not email or not password:
            QMessageBox.warning(
                self,
                "Error",
                "Por favor, complete todos los campos"
            )
            return
        
        try:
            token_data = self.cliente_api.iniciar_sesion(email, password)
            logger.info("Inicio de sesión exitoso")
            self.inicio_sesion_exitoso.emit(token_data)  # Emitir señal con los datos del token
            self.close()  # Cierra la ventana de login
            
        except Exception as e:
            logger.error(f"Error en el inicio de sesión: {str(e)}")
            QMessageBox.critical(
                self,
                "Error",
                "Error al iniciar sesión. Verifique sus credenciales."
            )
