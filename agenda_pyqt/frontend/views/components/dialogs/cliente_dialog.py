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
        self.corredor_input = QComboBox()
        self.observaciones_input = QTextEdit()
        self.observaciones_input.setMaximumHeight(100)

        # Cargar lista de corredores
        self.load_corredores()

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
            
            # Seleccionar el corredor en el combo box
            if cliente.get("corredor"):  
                index = self.corredor_input.findData(cliente["corredor"])
                if index >= 0:
                    self.corredor_input.setCurrentIndex(index)

        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", f"Error al cargar datos del cliente: {str(e)}")
            self.reject()

    def save_client(self):
        """Guarda los datos del cliente"""
        # Convertir fecha a formato MySQL o null si está vacía
        fecha_nac = self.fecha_nacimiento_input.date().toString("yyyy-MM-dd")
        if fecha_nac == "2025-01-19":  # Si es la fecha actual, la consideramos vacía
            fecha_nac = "0000-00-00"

        # Datos en el formato que espera el backend
        data = {
            "nombres": self.nombres_input.text().strip(),
            "apellidos": self.apellidos_input.text().strip(),
            "tipo_documento": self.tipo_documento_input.currentText(),
            "numero_documento": self.documento_input.text().strip(),
            "fecha_nacimiento": fecha_nac,
            "direccion": self.direccion_input.text().strip(),
            "localidad": self.localidad_input.text().strip(),
            "telefonos": self.telefonos_input.text().strip(),
            "movil": self.movil_input.text().strip(),
            "mail": self.mail_input.text().strip(),
            "corredor": self.corredor_input.currentData(),  
            "observaciones": self.observaciones_input.toPlainText().strip()
        }

        # Log de los datos que se enviarán
        logger.debug(f"Datos a enviar al backend: {data}")

        # Validaciones básicas - todos los campos requeridos según el error
        campos_requeridos = [
            "apellidos", "tipo_documento", "numero_documento", 
            "fecha_nacimiento", "direccion", "telefonos", 
            "movil", "mail"
        ]
        campos_vacios = [campo for campo in campos_requeridos if not data[campo]]
        
        if campos_vacios:
            campos = ", ".join(campos_vacios)
            QMessageBox.warning(self, "Error", f"Los siguientes campos son obligatorios: {campos}")
            return

        try:
            if self.client_id:  # Editar cliente existente
                response = requests.put(
                    f"http://localhost:8000/api/v1/clientes/{self.client_id}",
                    headers={"Authorization": f"Bearer {self.token}"},
                    json=data
                )
            else:  # Crear nuevo cliente
                logger.debug("Enviando solicitud POST para crear nuevo cliente")
                response = requests.post(
                    "http://localhost:8000/api/v1/clientes/",
                    headers={"Authorization": f"Bearer {self.token}"},
                    json=data
                )
            
            if response.status_code >= 400:
                logger.error(f"Error del servidor: {response.status_code}")
                logger.error(f"Respuesta del servidor: {response.text}")
                
            response.raise_for_status()
            QMessageBox.information(self, "Éxito", "Cliente guardado exitosamente")
            self.accept()

        except requests.RequestException as e:
            error_msg = f"Error al guardar cliente: {str(e)}"
            if hasattr(e.response, 'text'):
                error_msg += f"\nDetalles: {e.response.text}"
            logger.error(error_msg)
            QMessageBox.critical(self, "Error", error_msg)
