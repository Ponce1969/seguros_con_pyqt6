from PyQt6.QtWidgets import (QDialog, QFormLayout, QLineEdit, QTextEdit,
                            QPushButton, QHBoxLayout, QMessageBox)
from PyQt6.QtGui import QIntValidator
import requests
import logging

logger = logging.getLogger(__name__)

class CorredorDialog(QDialog):
    def __init__(self, parent=None, corredor_id=None, token=None):
        super().__init__(parent)
        self.token = token
        self.corredor_id = corredor_id
        self.setup_ui()
        
        if corredor_id:
            self.setWindowTitle("Editar Corredor")
            self.load_corredor_data()
        else:
            self.setWindowTitle("Agregar Corredor")

    def setup_ui(self):
        """Configura la interfaz del diálogo"""
        self.setMinimumWidth(400)
        layout = QFormLayout(self)
        layout.setSpacing(10)

        # Campos de entrada
        if self.corredor_id:
            # En modo edición, el número es un QLineEdit de solo lectura
            self.numero_input = QLineEdit()
            self.numero_input.setReadOnly(True)
            self.numero_input.setStyleSheet("QLineEdit { background-color: #f0f0f0; }")  # Fondo gris para indicar que no es editable
            numero_label = "Número de Corredor:"  # Sin asterisco ya que no se puede editar
        else:
            # En modo creación, el número es un QLineEdit editable
            self.numero_input = QLineEdit()
            self.numero_input.setValidator(QIntValidator(1, 99999))  # Solo permite números enteros
            numero_label = "Número de Corredor *:"
            
        self.nombres_input = QLineEdit()
        self.apellidos_input = QLineEdit()
        self.documento_input = QLineEdit()
        self.direccion_input = QLineEdit()
        self.localidad_input = QLineEdit()
        self.telefonos_input = QLineEdit()
        self.movil_input = QLineEdit()
        self.mail_input = QLineEdit()
        self.observaciones_input = QTextEdit()
        self.observaciones_input.setMaximumHeight(100)

        # Agregar campos al layout
        layout.addRow(numero_label, self.numero_input)
        layout.addRow("Nombres:", self.nombres_input)
        layout.addRow("Apellidos *:", self.apellidos_input)
        layout.addRow("Documento *:", self.documento_input)
        layout.addRow("Dirección *:", self.direccion_input)
        layout.addRow("Localidad *:", self.localidad_input)
        layout.addRow("Teléfonos:", self.telefonos_input)
        layout.addRow("Móvil:", self.movil_input)
        layout.addRow("Email *:", self.mail_input)
        layout.addRow("Observaciones:", self.observaciones_input)

        # Botones
        button_box = QHBoxLayout()
        save_button = QPushButton("Guardar")
        save_button.clicked.connect(self.save_corredor)
        cancel_button = QPushButton("Cancelar")
        cancel_button.clicked.connect(self.reject)
        
        button_box.addWidget(save_button)
        button_box.addWidget(cancel_button)
        layout.addRow(button_box)

    def load_corredor_data(self):
        """Carga los datos del corredor para edición"""
        try:
            response = requests.get(
                f"http://localhost:8000/api/v1/corredores/{self.corredor_id}",
                headers={"Authorization": f"Bearer {self.token}"}
            )
            response.raise_for_status()
            corredor = response.json()

            self.numero_input.setText(str(corredor["numero"]))
            self.nombres_input.setText(corredor.get("nombres", ""))
            self.apellidos_input.setText(corredor["apellidos"])
            self.documento_input.setText(corredor["documento"])
            self.direccion_input.setText(corredor["direccion"])
            self.localidad_input.setText(corredor["localidad"])
            self.telefonos_input.setText(corredor.get("telefonos", ""))
            self.movil_input.setText(corredor.get("movil", ""))
            self.mail_input.setText(corredor["mail"])
            self.observaciones_input.setText(corredor.get("observaciones", ""))

        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", f"Error al cargar datos del corredor: {str(e)}")
            self.reject()

    def save_corredor(self):
        """Guarda los datos del corredor"""
        try:
            # Validar campos requeridos
            if not all([
                self.apellidos_input.text().strip(),
                self.documento_input.text().strip(),
                self.direccion_input.text().strip(),
                self.localidad_input.text().strip(),
                self.mail_input.text().strip()
            ]):
                QMessageBox.warning(self, "Error", "Por favor complete todos los campos requeridos (*)")
                return

            # Si es un nuevo corredor, validar el número
            if not self.corredor_id:
                if not self.numero_input.text().strip():
                    QMessageBox.warning(self, "Error", "Por favor ingrese un número de corredor")
                    return
                try:
                    numero = int(self.numero_input.text().strip())
                    if numero <= 0:
                        QMessageBox.warning(self, "Error", "El número de corredor debe ser mayor a 0")
                        return
                except ValueError:
                    QMessageBox.warning(self, "Error", "El número de corredor debe ser un número entero")
                    return

            # Preparar datos
            data = {
                "nombres": self.nombres_input.text().strip(),
                "apellidos": self.apellidos_input.text().strip(),
                "documento": self.documento_input.text().strip(),
                "direccion": self.direccion_input.text().strip(),
                "localidad": self.localidad_input.text().strip(),
                "telefonos": self.telefonos_input.text().strip(),
                "movil": self.movil_input.text().strip(),
                "mail": self.mail_input.text().strip(),
                "observaciones": self.observaciones_input.toPlainText().strip()
            }

            # Solo incluir el número si es un nuevo corredor
            if not self.corredor_id:
                data["numero"] = int(self.numero_input.text().strip())

            logger.debug(f"Datos a enviar al backend: {data}")

            # Enviar datos al backend
            if self.corredor_id:
                response = requests.put(
                    f"http://localhost:8000/api/v1/corredores/{self.corredor_id}",
                    headers={"Authorization": f"Bearer {self.token}"},
                    json=data
                )
            else:
                response = requests.post(
                    "http://localhost:8000/api/v1/corredores/",
                    headers={"Authorization": f"Bearer {self.token}"},
                    json=data
                )

            response.raise_for_status()
            self.accept()

        except requests.RequestException as e:
            error_msg = f"Error al guardar corredor: {str(e)}"
            logger.error(error_msg)
            QMessageBox.critical(self, "Error", error_msg)
