from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QTextEdit, QMessageBox,
    QFormLayout
)
from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator

class CorredorForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.setup_connections()

    def setup_ui(self):
        form_layout = QFormLayout()
        
        # Campos de identificación
        self.numero_input = QLineEdit()
        self.numero_input.setPlaceholderText("Número único del corredor")
        # Solo permitir números
        validator = QRegularExpressionValidator(QRegularExpression("[0-9]+"))
        self.numero_input.setValidator(validator)
        
        self.nombres_input = QLineEdit()
        self.nombres_input.setPlaceholderText("Nombres del corredor")
        
        self.apellidos_input = QLineEdit()
        self.apellidos_input.setPlaceholderText("Apellidos del corredor")
        
        # Widget para documento
        self.documento_widget = QWidget()
        self.documento_layout = QHBoxLayout(self.documento_widget)
        self.documento_layout.setContentsMargins(0, 0, 0, 0)
        
        self.tipo_documento_combo = QComboBox()
        self.tipo_documento_combo.addItems(['DNI', 'CI', 'RUT', 'CUIT'])
        self.numero_documento_input = QLineEdit()
        self.numero_documento_input.setPlaceholderText("Número de documento")
        
        self.documento_layout.addWidget(self.tipo_documento_combo)
        self.documento_layout.addWidget(self.numero_documento_input)
        
        # Campos de contacto
        self.direccion_input = QLineEdit()
        self.direccion_input.setPlaceholderText("Dirección completa")
        
        self.localidad_input = QLineEdit()
        self.localidad_input.setPlaceholderText("Ciudad o localidad")
        
        self.telefonos_input = QLineEdit()
        self.telefonos_input.setPlaceholderText("Teléfono fijo")
        
        self.movil_input = QLineEdit()
        self.movil_input.setPlaceholderText("Teléfono móvil")
        
        self.mail_input = QLineEdit()
        self.mail_input.setPlaceholderText("correo@ejemplo.com")
        
        # Campo de observaciones
        self.observaciones_input = QTextEdit()
        self.observaciones_input.setPlaceholderText("Observaciones adicionales")
        self.observaciones_input.setMaximumHeight(100)
        
        # Agregar campos al formulario
        form_layout.addRow("Número:", self.numero_input)
        form_layout.addRow("Nombres:", self.nombres_input)
        form_layout.addRow("Apellidos:", self.apellidos_input)
        form_layout.addRow("Documento:", self.documento_widget)
        form_layout.addRow("Dirección:", self.direccion_input)
        form_layout.addRow("Localidad:", self.localidad_input)
        form_layout.addRow("Teléfono:", self.telefonos_input)
        form_layout.addRow("Móvil:", self.movil_input)
        form_layout.addRow("Mail:", self.mail_input)
        form_layout.addRow("Observaciones:", self.observaciones_input)
        
        self.setLayout(form_layout)

    def setup_connections(self):
        # Aquí se pueden agregar validaciones o conexiones de señales
        pass

    def get_data(self):
        """Obtiene los datos del formulario en formato diccionario"""
        tipo_doc = self.tipo_documento_combo.currentText()
        num_doc = self.numero_documento_input.text()
        documento = f"{tipo_doc} {num_doc}"
        
        return {
            "numero": int(self.numero_input.text()) if self.numero_input.text() else None,
            "nombres": self.nombres_input.text(),
            "apellidos": self.apellidos_input.text(),
            "documento": documento,
            "direccion": self.direccion_input.text(),
            "localidad": self.localidad_input.text(),
            "telefonos": self.telefonos_input.text(),
            "movil": self.movil_input.text(),
            "mail": self.mail_input.text(),
            "observaciones": self.observaciones_input.toPlainText()
        }

    def set_data(self, data):
        """Establece los datos del formulario desde un diccionario"""
        self.numero_input.setText(str(data.get("numero", "")))
        self.nombres_input.setText(data.get("nombres", ""))
        self.apellidos_input.setText(data.get("apellidos", ""))
        
        # Separar tipo y número de documento
        documento = data.get("documento", "")
        if documento:
            partes = documento.split(" ", 1)
            if len(partes) == 2:
                tipo_doc, num_doc = partes
                index = self.tipo_documento_combo.findText(tipo_doc)
                if index >= 0:
                    self.tipo_documento_combo.setCurrentIndex(index)
                self.numero_documento_input.setText(num_doc)
        
        self.direccion_input.setText(data.get("direccion", ""))
        self.localidad_input.setText(data.get("localidad", ""))
        self.telefonos_input.setText(data.get("telefonos", ""))
        self.movil_input.setText(data.get("movil", ""))
        self.mail_input.setText(data.get("mail", ""))
        self.observaciones_input.setPlainText(data.get("observaciones", ""))

    def clear(self):
        """Limpia todos los campos del formulario"""
        self.numero_input.clear()
        self.nombres_input.clear()
        self.apellidos_input.clear()
        self.numero_documento_input.clear()
        self.direccion_input.clear()
        self.localidad_input.clear()
        self.telefonos_input.clear()
        self.movil_input.clear()
        self.mail_input.clear()
        self.observaciones_input.clear()
