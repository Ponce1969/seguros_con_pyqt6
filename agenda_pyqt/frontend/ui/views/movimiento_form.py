from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QDateEdit, QTextEdit, QMessageBox,
    QFormLayout
)
from PyQt6.QtCore import QDate

class MovimientoForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.setup_connections()

    def setup_ui(self):
        form_layout = QFormLayout()
        
        # Campos del formulario
        self.fecha_mov_input = QDateEdit()
        self.corredor_input = QLineEdit()
        self.numero_cliente_compania_input = QLineEdit()
        self.tipo_seguro_input = QLineEdit()
        self.carpeta_input = QLineEdit()
        self.poliza_input = QLineEdit()
        self.endoso_input = QLineEdit()
        self.vto_desde_input = QDateEdit()
        self.vto_hasta_input = QDateEdit()
        self.moneda_input = QComboBox()
        self.premio_input = QLineEdit()
        self.cuotas_input = QLineEdit()
        self.observaciones_input = QTextEdit()
        
        # Configuración de campos
        self.fecha_mov_input.setCalendarPopup(True)
        self.fecha_mov_input.setDate(QDate.currentDate())
        self.vto_desde_input.setCalendarPopup(True)
        self.vto_hasta_input.setCalendarPopup(True)
        self.moneda_input.addItems(['$', 'U$S'])
        
        # Agregar campos al layout
        form_layout.addRow("Fecha Movimiento:", self.fecha_mov_input)
        form_layout.addRow("Corredor:", self.corredor_input)
        form_layout.addRow("Número Cliente Compania:", self.numero_cliente_compania_input)
        form_layout.addRow("Tipo Seguro:", self.tipo_seguro_input)
        form_layout.addRow("Carpeta:", self.carpeta_input)
        form_layout.addRow("Póliza:", self.poliza_input)
        form_layout.addRow("Endoso:", self.endoso_input)
        form_layout.addRow("Vigencia Desde:", self.vto_desde_input)
        form_layout.addRow("Vigencia Hasta:", self.vto_hasta_input)
        form_layout.addRow("Moneda:", self.moneda_input)
        form_layout.addRow("Premio:", self.premio_input)
        form_layout.addRow("Cuotas:", self.cuotas_input)
        form_layout.addRow("Observaciones:", self.observaciones_input)
        
        self.setLayout(form_layout)

    def setup_connections(self):
        self.premio_input.textChanged.connect(self.validar_numero)
        self.cuotas_input.textChanged.connect(self.validar_numero_entero)

    def validar_numero(self, texto):
        if not texto:
            return
        try:
            float(texto.replace(',', '.'))
        except ValueError:
            sender = self.sender()
            if isinstance(sender, QLineEdit):
                sender.setText(texto[:-1])

    def validar_numero_entero(self, texto):
        if not texto:
            return
        if not texto.isdigit():
            sender = self.sender()
            if isinstance(sender, QLineEdit):
                sender.setText(texto[:-1])

    def get_form_data(self):
        return {
            "fecha_mov": self.fecha_mov_input.date().toPyDate().isoformat(),
            "corredor": int(self.corredor_input.text()) if self.corredor_input.text() else None,
            "numero_cliente_compania": self.numero_cliente_compania_input.text(),
            "tipo_seguro": int(self.tipo_seguro_input.text()) if self.tipo_seguro_input.text() else None,
            "carpeta": self.carpeta_input.text(),
            "poliza": self.poliza_input.text(),
            "endoso": self.endoso_input.text(),
            "vto_desde": self.vto_desde_input.date().toPyDate().isoformat(),
            "vto_hasta": self.vto_hasta_input.date().toPyDate().isoformat(),
            "moneda": self.moneda_input.currentText(),
            "premio": float(self.premio_input.text().replace(',', '.')) if self.premio_input.text() else None,
            "cuotas": int(self.cuotas_input.text()) if self.cuotas_input.text() else None,
            "observaciones": self.observaciones_input.toPlainText()
        }

    def clear_form(self):
        self.fecha_mov_input.setDate(QDate.currentDate())
        self.corredor_input.clear()
        self.numero_cliente_compania_input.clear()
        self.tipo_seguro_input.clear()
        self.carpeta_input.clear()
        self.poliza_input.clear()
        self.endoso_input.clear()
        self.vto_desde_input.setDate(QDate.currentDate())
        self.vto_hasta_input.setDate(QDate.currentDate())
        self.moneda_input.setCurrentIndex(0)
        self.premio_input.clear()
        self.cuotas_input.clear()
        self.observaciones_input.clear()

    def set_form_data(self, data):
        self.fecha_mov_input.setDate(QDate.fromString(data.get("fecha_mov", ""), "yyyy-MM-dd"))
        self.corredor_input.setText(str(data.get("corredor", "")))
        self.numero_cliente_compania_input.setText(data.get("numero_cliente_compania", ""))
        self.tipo_seguro_input.setText(str(data.get("tipo_seguro", "")))
        self.carpeta_input.setText(data.get("carpeta", ""))
        self.poliza_input.setText(data.get("poliza", ""))
        self.endoso_input.setText(data.get("endoso", ""))
        self.vto_desde_input.setDate(QDate.fromString(data.get("vto_desde", ""), "yyyy-MM-dd"))
        self.vto_hasta_input.setDate(QDate.fromString(data.get("vto_hasta", ""), "yyyy-MM-dd"))
        self.moneda_input.setCurrentText(data.get("moneda", "$"))
        self.premio_input.setText(str(data.get("premio", "")))
        self.cuotas_input.setText(str(data.get("cuotas", "")))
        self.observaciones_input.setPlainText(data.get("observaciones", ""))
