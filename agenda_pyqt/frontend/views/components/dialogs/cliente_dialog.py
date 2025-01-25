from PyQt6.QtWidgets import (QDialog, QFormLayout, QLineEdit, QTextEdit,
                            QPushButton, QHBoxLayout, QMessageBox, QComboBox, QDateEdit)
from PyQt6.QtCore import QDate
import requests
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class ClienteDialog(QDialog):
    def __init__(self, parent=None, client_id=None, token=None):
        super().__init__(parent)
        self.token = token
        self.client_id = client_id
        self.setup_ui()
        
        if client_id:
            self.setWindowTitle("Editar Cliente")
            self.load_client_data()
        else:
            self.setWindowTitle("Agregar Cliente")

    def setup_ui(self):
        """Configura la interfaz del diálogo"""
        self.setMinimumWidth(400)
        layout = QFormLayout(self)
        layout.setSpacing(10)

        # Campos de entrada
        self.nombres_input = QLineEdit()
        self.apellidos_input = QLineEdit()
        self.tipo_documento_input = QComboBox()
        self.tipo_documento_input.addItems(["DNI", "CI", "RUT", "CUIT"])
        self.documento_input = QLineEdit()
        self.fecha_nacimiento_input = QDateEdit()
        self.fecha_nacimiento_input.setCalendarPopup(True)
        self.telefonos_input = QLineEdit()
        self.movil_input = QLineEdit()
        self.mail_input = QLineEdit()
        self.direccion_input = QLineEdit()
        self.localidad_input = QLineEdit()
        
        # Corredor input - QComboBox para nuevo cliente, QLineEdit para edición
        if self.client_id:
            self.corredor_input = QLineEdit()
            self.corredor_input.setReadOnly(True)  # No se puede editar
            self.corredor_input.setStyleSheet("QLineEdit { background-color: #f0f0f0; }")  # Fondo gris para indicar que no es editable
        else:
            self.corredor_input = QComboBox()
            self.load_corredores()  # Solo cargar corredores si es nuevo cliente
            
        self.observaciones_input = QTextEdit()
        self.observaciones_input.setMaximumHeight(100)

        # Agregar campos al layout
        layout.addRow("Nombres:", self.nombres_input)
        layout.addRow("Apellidos *:", self.apellidos_input)
        layout.addRow("Tipo Documento *:", self.tipo_documento_input)
        layout.addRow("Documento *:", self.documento_input)
        layout.addRow("Fecha Nacimiento:", self.fecha_nacimiento_input)
        layout.addRow("Teléfonos:", self.telefonos_input)
        layout.addRow("Móvil:", self.movil_input)
        layout.addRow("Email *:", self.mail_input)
        layout.addRow("Dirección *:", self.direccion_input)
        layout.addRow("Localidad *:", self.localidad_input)
        layout.addRow("Corredor:", self.corredor_input)
        layout.addRow("Observaciones:", self.observaciones_input)

        # Botones
        button_box = QHBoxLayout()
        save_button = QPushButton("Guardar")
        save_button.clicked.connect(self.save_client)
        cancel_button = QPushButton("Cancelar")
        cancel_button.clicked.connect(self.reject)
        
        button_box.addWidget(save_button)
        button_box.addWidget(cancel_button)
        layout.addRow(button_box)

    def load_corredores(self):
        """Carga la lista de corredores para el combo box"""
        try:
            response = requests.get(
                "http://localhost:8000/api/v1/corredores/",
                headers={"Authorization": f"Bearer {self.token}"}
            )
            response.raise_for_status()
            corredores = response.json()
            
            self.corredor_input.clear()
            self.corredor_input.addItem("Seleccione un corredor", None)
            
            for corredor in corredores:
                self.corredor_input.addItem(
                    f"{corredor['apellidos']}, {corredor.get('nombres', '')} ({corredor['numero']})",
                    corredor['numero']
                )
                
        except requests.RequestException as e:
            logger.error(f"Error al cargar corredores: {str(e)}")
            QMessageBox.warning(self, "Error", "No se pudieron cargar los corredores")

    def load_client_data(self):
        """Carga los datos del cliente para edición"""
        try:
            response = requests.get(
                f"http://localhost:8000/api/v1/clientes/{self.client_id}",
                headers={"Authorization": f"Bearer {self.token}"}
            )
            response.raise_for_status()
            cliente = response.json()

            self.nombres_input.setText(cliente.get("nombres", ""))
            self.apellidos_input.setText(cliente["apellidos"])
            self.documento_input.setText(cliente.get("numero_documento", ""))
            
            # Fecha de nacimiento
            if cliente.get("fecha_nacimiento") and cliente["fecha_nacimiento"] != "0000-00-00":
                fecha = datetime.strptime(cliente["fecha_nacimiento"], "%Y-%m-%d")
                self.fecha_nacimiento_input.setDate(QDate(fecha.year, fecha.month, fecha.day))
            else:
                self.fecha_nacimiento_input.setDate(QDate.currentDate())
                
            self.telefonos_input.setText(cliente.get("telefonos", ""))
            self.movil_input.setText(cliente.get("movil", ""))
            self.mail_input.setText(cliente.get("mail", ""))
            self.direccion_input.setText(cliente.get("direccion", ""))
            self.localidad_input.setText(cliente.get("localidad", ""))
            self.observaciones_input.setText(cliente.get("observaciones", ""))
            
            # Mostrar el corredor en el QLineEdit
            corredor_numero = cliente.get("corredor")
            if corredor_numero:
                try:
                    response = requests.get(
                        f"http://localhost:8000/api/v1/corredores/{corredor_numero}",
                        headers={"Authorization": f"Bearer {self.token}"}
                    )
                    response.raise_for_status()
                    corredor = response.json()
                    self.corredor_input.setText(f"{corredor['apellidos']}, {corredor.get('nombres', '')} ({corredor['numero']})")
                except:
                    self.corredor_input.setText(f"Corredor #{corredor_numero}")
            
            # Seleccionar tipo de documento
            tipo_doc = cliente.get("tipo_documento", "DNI")
            index = self.tipo_documento_input.findText(tipo_doc)
            if index >= 0:
                self.tipo_documento_input.setCurrentIndex(index)
                
        except requests.RequestException as e:
            logger.error(f"Error al cargar datos del cliente: {str(e)}")
            QMessageBox.critical(self, "Error", "No se pudieron cargar los datos del cliente")
            self.reject()

    def save_client(self):
        """Guarda los datos del cliente"""
        try:
            # Validar campos requeridos
            if not all([
                self.apellidos_input.text().strip(),
                self.documento_input.text().strip(),
                self.mail_input.text().strip(),
                self.direccion_input.text().strip(),
                self.localidad_input.text().strip()
            ]):
                QMessageBox.warning(self, "Error", "Por favor complete todos los campos requeridos (*)")
                return

            # Preparar datos
            data = {
                "nombres": self.nombres_input.text(),
                "apellidos": self.apellidos_input.text(),
                "tipo_documento": self.tipo_documento_input.currentText(),
                "numero_documento": self.documento_input.text(),
                "fecha_nacimiento": self.fecha_nacimiento_input.date().toString("yyyy-MM-dd"),
                "direccion": self.direccion_input.text(),
                "localidad": self.localidad_input.text(),
                "telefonos": self.telefonos_input.text(),
                "movil": self.movil_input.text(),
                "mail": self.mail_input.text(),
                "observaciones": self.observaciones_input.toPlainText()
            }
            
            # Si es un nuevo cliente, agregar el corredor seleccionado
            if not self.client_id:
                corredor_id = self.corredor_input.currentData()
                if not corredor_id:
                    QMessageBox.warning(self, "Error", "Por favor seleccione un corredor")
                    return
                data["corredor"] = corredor_id
            
            logger.debug(f"Datos a enviar al backend: {data}")
            
            # Enviar datos al backend
            if self.client_id:
                response = requests.put(
                    f"http://localhost:8000/api/v1/clientes/{self.client_id}",
                    headers={"Authorization": f"Bearer {self.token}"},
                    json=data
                )
            else:
                response = requests.post(
                    "http://localhost:8000/api/v1/clientes/",
                    headers={"Authorization": f"Bearer {self.token}"},
                    json=data
                )
            
            response.raise_for_status()
            self.accept()
            
        except requests.RequestException as e:
            error_msg = f"Error al guardar cliente: {str(e)}"
            logger.error(error_msg)
            QMessageBox.critical(self, "Error", error_msg)
