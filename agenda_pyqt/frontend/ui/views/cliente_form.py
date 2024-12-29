from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QDateEdit, QTextEdit, QMessageBox,
    QFormLayout
)
from PyQt6.QtCore import QDate, QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator

class ClienteForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.setup_connections()

    def setup_ui(self):
        form_layout = QFormLayout()
        
        # Campos del formulario
        self.nombres_input = QLineEdit()
        self.apellidos_input = QLineEdit()
        
        # Crear un widget horizontal para documento
        self.documento_widget = QWidget()
        self.documento_layout = QHBoxLayout(self.documento_widget)
        
        # Crear ComboBox para tipo de documento
        self.tipo_documento_combo = QComboBox()
        self.tipo_documento_combo.addItems(['DNI', 'CI', 'RUT', 'CUIT'])
        
        # Crear LineEdit para número de documento
        self.documentos_input = QLineEdit()
        self.documentos_input.setMaxLength(20)  # Permitir hasta 20 caracteres
        self.documentos_input.setPlaceholderText("Ingrese número de documento")
        
        # Validador para permitir solo números y guiones
        validator = QRegularExpressionValidator(QRegularExpression("[0-9-]{0,20}"))
        self.documentos_input.setValidator(validator)
        
        # Agregar widgets al layout horizontal
        self.documento_layout.addWidget(self.tipo_documento_combo)
        self.documento_layout.addWidget(self.documentos_input)
        
        self.fecha_nacimiento_input = QDateEdit()
        self.direccion_input = QLineEdit()
        self.localidad_input = QLineEdit()
        self.telefonos_input = QLineEdit()
        self.movil_input = QLineEdit()
        self.mail_input = QLineEdit()
        self.corredor_input = QLineEdit()
        self.observaciones_input = QTextEdit()
        
        # Configuración de campos
        self.fecha_nacimiento_input.setCalendarPopup(True)
        self.fecha_nacimiento_input.setDate(QDate.currentDate())
        
        # Agregar campos al layout
        form_layout.addRow("Nombres:", self.nombres_input)
        form_layout.addRow("Apellidos:", self.apellidos_input)
        form_layout.addRow("Documento:", self.documento_widget)
        form_layout.addRow("Fecha de Nacimiento:", self.fecha_nacimiento_input)
        form_layout.addRow("Dirección:", self.direccion_input)
        form_layout.addRow("Localidad:", self.localidad_input)
        form_layout.addRow("Teléfonos:", self.telefonos_input)
        form_layout.addRow("Móvil:", self.movil_input)
        form_layout.addRow("Email:", self.mail_input)
        form_layout.addRow("Corredor:", self.corredor_input)
        form_layout.addRow("Observaciones:", self.observaciones_input)
        
        self.setLayout(form_layout)

    def setup_connections(self):
        self.telefonos_input.textChanged.connect(self.validar_telefono)
        self.movil_input.textChanged.connect(self.validar_telefono)
        self.mail_input.textChanged.connect(self.validar_email)

    def validar_telefono(self, texto):
        sender = self.sender()
        if not isinstance(sender, QLineEdit):
            return
        
        texto_limpio = ''.join(c for c in texto if c.isdigit() or c in '+- ()')
        
        if texto != texto_limpio:
            sender.blockSignals(True)
            sender.setText(texto_limpio)
            sender.blockSignals(False)
            
        if len(texto_limpio.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')) > 15:
            sender.blockSignals(True)
            sender.setText(texto_limpio[:-1])
            sender.blockSignals(False)

    def validar_email(self, texto):
        # Implementar validación de email aquí
        pass

    def get_form_data(self):
        return {
            "nombres": self.nombres_input.text(),
            "apellidos": self.apellidos_input.text(),
            "tipo_documento": self.tipo_documento_combo.currentText(),
            "documentos": self.documentos_input.text(),
            "fecha_nacimiento": self.fecha_nacimiento_input.date().toPyDate().isoformat(),
            "direccion": self.direccion_input.text(),
            "localidad": self.localidad_input.text(),
            "telefonos": self.telefonos_input.text(),
            "movil": self.movil_input.text(),
            "mail": self.mail_input.text(),
            "corredor": self.corredor_input.text(),
            "observaciones": self.observaciones_input.toPlainText(),
            "usuario_id": 1  # Este valor debería venir de la sesión del usuario
        }

    def clear_form(self):
        self.nombres_input.clear()
        self.apellidos_input.clear()
        self.tipo_documento_combo.setCurrentIndex(0)
        self.documentos_input.clear()
        self.fecha_nacimiento_input.setDate(QDate.currentDate())
        self.direccion_input.clear()
        self.localidad_input.clear()
        self.telefonos_input.clear()
        self.movil_input.clear()
        self.mail_input.clear()
        self.corredor_input.clear()
        self.observaciones_input.clear()

    def set_form_data(self, data):
        if data is None:
            self.clear_form()
            return
            
        self.nombres_input.setText(data.get("nombres", ""))
        self.apellidos_input.setText(data.get("apellidos", ""))
        self.tipo_documento_combo.setCurrentText(data.get("tipo_documento", ""))
        self.documentos_input.setText(data.get("documentos", ""))
        
        # Convertir la fecha de string a QDate si existe
        fecha_str = data.get("fecha_nacimiento", "")
        if fecha_str:
            try:
                fecha = QDate.fromString(fecha_str, "yyyy-MM-dd")
                self.fecha_nacimiento_input.setDate(fecha)
            except:
                self.fecha_nacimiento_input.setDate(QDate.currentDate())
        
        self.direccion_input.setText(data.get("direccion", ""))
        self.localidad_input.setText(data.get("localidad", ""))
        self.telefonos_input.setText(data.get("telefonos", ""))
        self.movil_input.setText(data.get("movil", ""))
        self.mail_input.setText(data.get("mail", ""))
        self.corredor_input.setText(data.get("corredor", ""))
        self.observaciones_input.setPlainText(data.get("observaciones", ""))
