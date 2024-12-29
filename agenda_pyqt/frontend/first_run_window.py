from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QFormLayout, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import requests
import logging
import json

logger = logging.getLogger(__name__)

class FirstRunWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.app = None  # Se establecerá después de la creación
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('Configuración Inicial')
        self.setGeometry(100, 100, 500, 400)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Título
        title_label = QLabel("Bienvenido al Sistema de Seguros")
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(14)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Descripción
        desc_label = QLabel("Por favor, configure el usuario administrador inicial:")
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(desc_label)
        
        # Formulario
        form_layout = QFormLayout()
        
        # Campos del formulario
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nombre completo")
        form_layout.addRow("Nombre:", self.name_input)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("correo@ejemplo.com")
        form_layout.addRow("Email:", self.email_input)
        
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Mínimo 8 caracteres")
        form_layout.addRow("Contraseña:", self.password_input)
        
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_password_input.setPlaceholderText("Repita la contraseña")
        form_layout.addRow("Confirmar Contraseña:", self.confirm_password_input)
        
        main_layout.addLayout(form_layout)
        
        # Botón de configuración
        button_layout = QHBoxLayout()
        self.setup_button = QPushButton("Configurar Administrador")
        self.setup_button.clicked.connect(self.handle_setup)
        button_layout.addWidget(self.setup_button)
        main_layout.addLayout(button_layout)
        
        # Centrar la ventana
        self.center()
    
    def center(self):
        """Centra la ventana en la pantalla"""
        frame_geometry = self.frameGeometry()
        screen_center = self.screen().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())
    
    def handle_setup(self):
        """Maneja la configuración inicial del administrador"""
        name = self.name_input.text()
        email = self.email_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()
        
        if not all([name, email, password, confirm_password]):
            QMessageBox.warning(self, 'Error', 'Por favor complete todos los campos')
            return
        
        if password != confirm_password:
            QMessageBox.warning(self, 'Error', 'Las contraseñas no coinciden')
            return
        
        if len(password) < 8:
            QMessageBox.warning(self, 'Error', 'La contraseña debe tener al menos 8 caracteres')
            return
        
        try:
            # Preparar los datos
            data = {
                'name': name,
                'email': email,
                'password': password,
                'role': 'admin',
                'comision_porcentaje': 0.0
            }
            
            # Hacer la petición
            response = requests.post(
                'http://localhost:8000/users/setup-admin',
                json=data
            )
            
            # Registrar la respuesta para debugging
            logger.debug(f"Status Code: {response.status_code}")
            logger.debug(f"Response Text: {response.text}")
            
            if response.status_code == 200:
                QMessageBox.information(
                    self,
                    'Éxito',
                    'Administrador configurado correctamente. Por favor, inicie sesión.'
                )
                self.app.show_login_window()
            else:
                try:
                    error_data = response.json()
                    error_msg = error_data.get('detail', 'Error desconocido')
                except json.JSONDecodeError:
                    error_msg = response.text or 'Error desconocido'
                
                QMessageBox.warning(self, 'Error', error_msg)
        
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(
                self,
                'Error de Conexión',
                'No se pudo conectar con el servidor. Por favor, verifica que el servidor esté funcionando.'
            )
        except Exception as e:
            logger.exception("Error inesperado durante la configuración del administrador")
            QMessageBox.critical(
                self,
                'Error',
                f'Error inesperado: {str(e)}'
            )
