"""
Dialog para gestión de usuarios.
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit,
    QPushButton, QMessageBox, QCheckBox
)
from PyQt6.QtCore import Qt

class UserDialog(QDialog):
    def __init__(self, parent=None, api_client=None):
        super().__init__(parent)
        self.api_client = api_client
        self.setup_ui()

    def setup_ui(self):
        """Configurar la interfaz de usuario."""
        self.setWindowTitle("Gestión de Usuario")
        self.setModal(True)
        
        # Layout principal
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()
        
        # Campos
        self.username_edit = QLineEdit()
        self.email_edit = QLineEdit()
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        
        # Solo visible para superusuarios
        self.is_superuser_check = QCheckBox("Es administrador")
        self.is_superuser_check.setVisible(False)  # Por defecto oculto
        
        # Agregar campos al formulario
        form_layout.addRow("Usuario:", self.username_edit)
        form_layout.addRow("Email:", self.email_edit)
        form_layout.addRow("Contraseña:", self.password_edit)
        form_layout.addRow(self.is_superuser_check)
        
        # Botones
        self.save_button = QPushButton("Guardar")
        self.save_button.clicked.connect(self.save_user)
        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.clicked.connect(self.reject)
        
        # Agregar layouts
        layout.addLayout(form_layout)
        layout.addWidget(self.save_button)
        layout.addWidget(self.cancel_button)

    def set_superuser_mode(self, is_superuser: bool):
        """Habilitar/deshabilitar opciones de superusuario."""
        self.is_superuser_check.setVisible(is_superuser)

    async def save_user(self):
        """Guardar el usuario."""
        try:
            data = {
                "username": self.username_edit.text(),
                "email": self.email_edit.text(),
                "password": self.password_edit.text(),
                "is_superuser": self.is_superuser_check.isChecked()
            }
            
            # Validaciones básicas
            if not data["username"] or not data["email"] or not data["password"]:
                QMessageBox.warning(
                    self,
                    "Error",
                    "Todos los campos son obligatorios"
                )
                return
            
            # Crear usuario
            response = await self.api_client.post("/users/", json=data)
            if response.status_code == 200:
                QMessageBox.information(
                    self,
                    "Éxito",
                    "Usuario creado correctamente"
                )
                self.accept()
            else:
                QMessageBox.warning(
                    self,
                    "Error",
                    f"Error al crear usuario: {response.text}"
                )
                
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Error inesperado: {str(e)}"
            )
