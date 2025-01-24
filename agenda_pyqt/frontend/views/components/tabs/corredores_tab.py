from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                            QPushButton, QTableWidget, QTableWidgetItem,
                            QMessageBox)
from PyQt6.QtCore import Qt
from ..dialogs.corredor_dialog import CorredorDialog
import requests
import logging

logger = logging.getLogger(__name__)

class CorredoresTab(QWidget):
    def __init__(self, token):
        super().__init__()
        self.token = token
        self.setup_ui()
        
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Título
        title_label = QLabel("Gestión de Corredores")
        title_label.setStyleSheet("font-size: 14pt; font-weight: bold;")
        layout.addWidget(title_label)
        
        # Barra de herramientas
        toolbar = QHBoxLayout()
        toolbar.setSpacing(10)
        
        add_button = QPushButton("Agregar Corredor")
        add_button.setFixedWidth(150)
        add_button.clicked.connect(self.show_add_corredor_dialog)
        toolbar.addWidget(add_button)
        
        refresh_button = QPushButton("Actualizar Lista")
        refresh_button.setFixedWidth(150)
        refresh_button.clicked.connect(self.load_corredores)
        toolbar.addWidget(refresh_button)
        
        toolbar.addStretch()
        layout.addLayout(toolbar)
        
        # Tabla de corredores
        self.setup_table()
        layout.addWidget(self.corredores_table)
        
        # Cargar corredores
        self.load_corredores()
        
    def setup_table(self):
        """Configura la tabla de corredores"""
        self.corredores_table = QTableWidget()
        self.corredores_table.setColumnCount(10)
        self.corredores_table.setHorizontalHeaderLabels([
            "Número", "Nombres", "Apellidos", "Documento", 
            "Dirección", "Localidad", "Teléfonos",
            "Móvil", "Email", "Acciones"
        ])
        
        # Configurar la tabla
        header = self.corredores_table.horizontalHeader()
        header.setStretchLastSection(True)
        for i in range(9):  # Todas las columnas excepto Acciones
            header.setSectionResizeMode(i, header.ResizeMode.ResizeToContents)
        
        self.corredores_table.verticalHeader().setVisible(False)
        self.corredores_table.setAlternatingRowColors(True)
        self.corredores_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.corredores_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.corredores_table.setMinimumHeight(300)

    def load_corredores(self):
        """Carga los corredores desde la API"""
        try:
            logger.debug(f"Intentando cargar corredores con token: {self.token[:10]}...")
            response = requests.get(
                "http://localhost:8000/api/v1/corredores/",
                headers={"Authorization": f"Bearer {self.token}"}
            )
            logger.debug(f"Respuesta del servidor: {response.status_code}")
            
            response.raise_for_status()
            corredores = response.json()
            logger.debug(f"Corredores cargados: {len(corredores)}")
            
            self.corredores_table.setRowCount(0)
            
            if not corredores:
                logger.debug("No se encontraron corredores")
                self.corredores_table.setRowCount(1)
                empty_message = QTableWidgetItem("No hay corredores registrados")
                empty_message.setFlags(Qt.ItemFlag.ItemIsEnabled)
                empty_message.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.corredores_table.setSpan(0, 0, 1, 10)
                self.corredores_table.setItem(0, 0, empty_message)
                return
            
            for corredor in corredores:
                self.add_corredor_to_table(corredor)
            
            # Ajustar el tamaño de las filas
            self.corredores_table.resizeRowsToContents()
            logger.debug("Tabla de corredores actualizada exitosamente")
                
        except requests.RequestException as e:
            error_msg = f"Error al cargar corredores: {str(e)}"
            logger.error(error_msg)
            QMessageBox.critical(self, "Error", error_msg)
            
    def add_corredor_to_table(self, corredor):
        """Añade un corredor a la tabla"""
        row = self.corredores_table.rowCount()
        self.corredores_table.insertRow(row)
        
        # Añadir datos del corredor
        items = [
            QTableWidgetItem(str(corredor["numero"])),
            QTableWidgetItem(corredor.get("nombres", "")),
            QTableWidgetItem(corredor["apellidos"]),
            QTableWidgetItem(corredor["documento"]),
            QTableWidgetItem(corredor["direccion"]),
            QTableWidgetItem(corredor["localidad"]),
            QTableWidgetItem(corredor.get("telefonos", "")),
            QTableWidgetItem(corredor.get("movil", "")),
            QTableWidgetItem(corredor["mail"])
        ]
        
        # Configurar items
        for col, item in enumerate(items):
            item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
            if col == 0:  # Número de corredor
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.corredores_table.setItem(row, col, item)
        
        # Botones de acción
        action_widget = QWidget()
        action_layout = QHBoxLayout(action_widget)
        action_layout.setContentsMargins(5, 0, 5, 0)
        action_layout.setSpacing(5)
        
        edit_button = QPushButton("Editar")
        edit_button.setFixedWidth(60)
        edit_button.setStyleSheet("background-color: #4CAF50; color: white;")
        numero = corredor["numero"]
        edit_button.clicked.connect(lambda checked, num=numero: self.show_edit_corredor_dialog(num))
        action_layout.addWidget(edit_button)
        
        delete_button = QPushButton("Eliminar")
        delete_button.setFixedWidth(60)
        delete_button.setStyleSheet("background-color: #f44336; color: white;")
        delete_button.clicked.connect(lambda checked, num=numero: self.delete_corredor(num))
        action_layout.addWidget(delete_button)
        
        self.corredores_table.setCellWidget(row, 9, action_widget)

    def show_add_corredor_dialog(self):
        """Muestra el diálogo para agregar un nuevo corredor"""
        dialog = CorredorDialog(parent=self, token=self.token)
        if dialog.exec() == dialog.DialogCode.Accepted:
            self.load_corredores()

    def show_edit_corredor_dialog(self, corredor_id):
        """Muestra el diálogo para editar un corredor existente"""
        dialog = CorredorDialog(parent=self, corredor_id=corredor_id, token=self.token)
        if dialog.exec() == dialog.DialogCode.Accepted:
            self.load_corredores()

    def delete_corredor(self, corredor_id):
        """Elimina un corredor"""
        reply = QMessageBox.question(
            self,
            "Confirmar eliminación",
            "¿Está seguro de que desea eliminar este corredor?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                response = requests.delete(
                    f"http://localhost:8000/api/v1/corredores/{corredor_id}",
                    headers={"Authorization": f"Bearer {self.token}"}
                )
                response.raise_for_status()
                self.load_corredores()
                QMessageBox.information(self, "Éxito", "Corredor eliminado exitosamente")
            except requests.RequestException as e:
                QMessageBox.critical(self, "Error", f"Error al eliminar corredor: {str(e)}")
