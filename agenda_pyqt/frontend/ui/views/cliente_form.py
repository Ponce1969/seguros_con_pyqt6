from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QDateEdit, QTextEdit, QMessageBox,
    QFormLayout
)
from PyQt6.QtCore import QDate, QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
import requests

class ClienteForm(QWidget):
    def __init__(self, parent=None, cliente_api=None):
        super().__init__(parent)
        self.cliente_api = cliente_api
        self.setup_ui()
        self.setup_connections()
        self.cargar_corredores()

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
        self.numero_documento_input = QLineEdit()  
        self.numero_documento_input.setMaxLength(20)  
        self.numero_documento_input.setPlaceholderText("Ingrese número de documento")
        
        # Validador para permitir solo números y guiones
        validator = QRegularExpressionValidator(QRegularExpression("[0-9-]{0,20}"))
        self.numero_documento_input.setValidator(validator)
        
        # Agregar widgets al layout horizontal
        self.documento_layout.addWidget(self.tipo_documento_combo)
        self.documento_layout.addWidget(self.numero_documento_input)
        
        self.fecha_nacimiento_input = QDateEdit()
        self.direccion_input = QLineEdit()
        self.localidad_input = QLineEdit()
        self.telefonos_input = QLineEdit()
        self.movil_input = QLineEdit()
        self.mail_input = QLineEdit()
        
        # Reemplazar LineEdit por ComboBox para corredores
        self.corredor_combo = QComboBox()
        self.corredor_combo.setPlaceholderText("Seleccione un corredor")
        
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
        form_layout.addRow("Mail:", self.mail_input)
        form_layout.addRow("Corredor:", self.corredor_combo)
        form_layout.addRow("Observaciones:", self.observaciones_input)
        
        self.setLayout(form_layout)

    def cargar_corredores(self):
        """Carga la lista de corredores en el ComboBox"""
        try:
            if self.cliente_api:
                # Limpiar el combo box
                self.corredor_combo.clear()
                
                # Agregar un item por defecto
                self.corredor_combo.addItem("-- Seleccione un corredor --", None)
                
                try:
                    corredores = self.cliente_api.obtener_corredores()
                    if corredores:
                        for corredor in corredores:
                            # Mostrar número y nombre del corredor
                            self.corredor_combo.addItem(
                                f"{corredor['numero']} - {corredor['nombres']} {corredor['apellidos']}", 
                                corredor['numero']
                            )
                except requests.exceptions.RequestException as e:
                    # Si no hay corredores o hay un error, no mostrar mensaje de error
                    # Solo dejar el item por defecto
                    pass
                    
                # Seleccionar el item por defecto
                self.corredor_combo.setCurrentIndex(0)
        except Exception as e:
            # Solo mostrar error si es un error inesperado
            QMessageBox.warning(self, "Error", f"Error inesperado al cargar corredores: {str(e)}")

    def setup_connections(self):
        self.telefonos_input.textChanged.connect(self.validar_telefono)
        self.movil_input.textChanged.connect(self.validar_telefono)
        self.mail_input.textChanged.connect(self.validar_mail)

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

    def validar_mail(self, texto):
        # Implementar validación de mail aquí
        pass

    def get_form_data(self):
        # Obtener el número de corredor del item seleccionado
        corredor_id = self.corredor_combo.currentData()
        
        # Validar que se haya seleccionado un corredor
        if corredor_id is None:
            raise ValueError("Debe seleccionar un corredor")
            
        return {
            "nombres": self.nombres_input.text(),
            "apellidos": self.apellidos_input.text(),
            "tipo_documento": self.tipo_documento_combo.currentText(),
            "numero_documento": self.numero_documento_input.text(),  
            "fecha_nacimiento": self.fecha_nacimiento_input.date().toPyDate().isoformat(),
            "direccion": self.direccion_input.text(),
            "localidad": self.localidad_input.text(),
            "telefonos": self.telefonos_input.text(),
            "movil": self.movil_input.text(),
            "mail": self.mail_input.text(),
            "corredor": corredor_id,
            "observaciones": self.observaciones_input.toPlainText(),
            "usuario_id": 1  
        }

    def clear_form(self):
        self.nombres_input.clear()
        self.apellidos_input.clear()
        self.tipo_documento_combo.setCurrentIndex(0)
        self.numero_documento_input.clear()  
        self.fecha_nacimiento_input.setDate(QDate.currentDate())
        self.direccion_input.clear()
        self.localidad_input.clear()
        self.telefonos_input.clear()
        self.movil_input.clear()
        self.mail_input.clear()
        self.corredor_combo.setCurrentIndex(-1)  # Ningún corredor seleccionado
        self.observaciones_input.clear()

    def set_form_data(self, data):
        if data is None:
            self.clear_form()
            return
            
        self.nombres_input.setText(data.get("nombres", ""))
        self.apellidos_input.setText(data.get("apellidos", ""))
        self.tipo_documento_combo.setCurrentText(data.get("tipo_documento", ""))
        self.numero_documento_input.setText(data.get("numero_documento", ""))  
        
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
        
        # Seleccionar el corredor correcto en el ComboBox
        corredor_id = data.get("corredor")
        if corredor_id is not None:
            index = self.corredor_combo.findData(corredor_id)
            if index >= 0:
                self.corredor_combo.setCurrentIndex(index)
