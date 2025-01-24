from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel,
                            QLineEdit, QPushButton, QMessageBox, QSizePolicy,
                            QApplication)
from PyQt6.QtCore import Qt
import requests
import logging

logger = logging.getLogger(__name__)

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.app = None  # Se establecerá después de la creación
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('Login')
        self.setGeometry(100, 100, 400, 200)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Elementos de la interfaz
        self.email_label = QLabel('Email:')
        self.email_input = QLineEdit()
        self.password_label = QLabel('Contraseña:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.login_button = QPushButton('Iniciar Sesión')
        
        # Agregar elementos al layout
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        
        # Conectar señales
        self.login_button.clicked.connect(self.handle_login)
        self.password_input.returnPressed.connect(self.handle_login)
        
        # Centrar la ventana
        self.center()
    
    def center(self):
        """Centra la ventana en la pantalla"""
        frame_geometry = self.frameGeometry()
        screen_center = self.screen().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())
    
    def handle_login(self):
        """Maneja el intento de inicio de sesión"""
        email = self.email_input.text()
        password = self.password_input.text()
        
        if not email or not password:
            QMessageBox.warning(self, 'Error', 'Por favor ingrese email y contraseña')
            return
        
        try:
            response = requests.post(
                'http://localhost:8000/api/v1/iniciar-sesion/token',
                data={'username': email, 'password': password}
            )
            
            if response.status_code == 200:
                token_data = response.json()
                token = token_data['access_token']
                self.app.set_auth_token(token)
                logger.debug(f"Token obtenido exitosamente: {token[:10]}...")  # Solo para debug
            else:
                error_msg = response.json().get('detail', 'Error desconocido')
                QMessageBox.warning(self, 'Error de Login', error_msg)
                logger.error(f"Error en login: {error_msg}")
                
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(
                self,
                'Error de Conexión',
                'No se pudo conectar con el servidor. Por favor, verifica que el servidor esté funcionando.'
            )
            logger.error("Error de conexión al servidor")
        except Exception as e:
            QMessageBox.critical(
                self,
                'Error',
                f'Error inesperado: {str(e)}'
            )
            logger.error(f"Error inesperado en login: {str(e)}")
