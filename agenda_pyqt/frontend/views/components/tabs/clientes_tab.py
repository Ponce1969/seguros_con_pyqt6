from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                            QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView)
from PyQt6.QtCore import Qt
from ..dialogs.cliente_dialog import ClienteDialog
import requests
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class ClientesTab(QWidget):
    def __init__(self, token):
        super().__init__()
        self.token = token
        self.setup_ui()
        
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Barra de herramientas
        toolbar = QHBoxLayout()
        toolbar.setSpacing(10)
        
        # Botones principales
        add_button = QPushButton("Agregar Cliente")
        add_button.setFixedWidth(120)
        add_button.clicked.connect(self.show_add_client_dialog)
        toolbar.addWidget(add_button)
        
        # Botones de acción (desactivados por defecto)
        self.edit_button = QPushButton("Editar")
        self.edit_button.setFixedWidth(80)
        self.edit_button.setEnabled(False)
        self.edit_button.clicked.connect(self.edit_selected_client)
        toolbar.addWidget(self.edit_button)
        
        self.delete_button = QPushButton("Eliminar")
        self.delete_button.setFixedWidth(80)
        self.delete_button.setEnabled(False)
        self.delete_button.clicked.connect(self.delete_selected_client)
        toolbar.addWidget(self.delete_button)
        
        refresh_button = QPushButton("Actualizar Lista")
        refresh_button.setFixedWidth(120)
        refresh_button.clicked.connect(self.load_clients)
        toolbar.addWidget(refresh_button)
        
        toolbar.addStretch()
        layout.addLayout(toolbar)
        
        # Tabla de clientes
        self.setup_table()
        layout.addWidget(self.clients_table)
        
        # Cargar clientes
        self.load_clients()
        
    def setup_table(self):
        """Configura la tabla de clientes"""
        self.clients_table = QTableWidget()
        self.clients_table.setColumnCount(11)  # Eliminada la columna de acciones
        self.clients_table.setHorizontalHeaderLabels([
            "ID", "Nombres", "Apellidos", "Tipo Doc.", "Documento",
            "Fecha Nac.", "Teléfonos", "Móvil", "Email", "Dirección",
            "Localidad"
        ])
        
        # Configurar la tabla
        header = self.clients_table.horizontalHeader()
        header.setStretchLastSection(True)
        for i in range(11):
            header.setSectionResizeMode(i, header.ResizeMode.ResizeToContents)
        
        self.clients_table.verticalHeader().setVisible(False)
        self.clients_table.setAlternatingRowColors(True)
        self.clients_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.clients_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.clients_table.setMinimumHeight(300)
        
        # Conectar evento de selección
        self.clients_table.itemSelectionChanged.connect(self.on_selection_changed)
        
    def load_clients(self):
        """Carga los clientes desde la API"""
        try:
            logger.debug("Intentando cargar clientes...")
            response = requests.get(
                "http://localhost:8000/api/v1/clientes/",
                headers={"Authorization": f"Bearer {self.token}"}
            )
            logger.debug(f"Respuesta del servidor: {response.status_code}")
            
            response.raise_for_status()
            clientes = response.json()
            logger.debug(f"Clientes cargados: {len(clientes)}")
            
            self.clients_table.setRowCount(0)
            
            if not clientes:
                logger.debug("No se encontraron clientes")
                self.clients_table.setRowCount(1)
                empty_message = QTableWidgetItem("No hay clientes registrados")
                empty_message.setFlags(Qt.ItemFlag.ItemIsEnabled)
                empty_message.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.clients_table.setSpan(0, 0, 1, 11)
                self.clients_table.setItem(0, 0, empty_message)
                return
            
            for cliente in clientes:
                self.add_client_to_table(cliente)
            
            # Ajustar el tamaño de las filas
            self.clients_table.resizeRowsToContents()
            logger.debug("Tabla de clientes actualizada exitosamente")
                
        except requests.RequestException as e:
            error_msg = f"Error al cargar clientes: {str(e)}"
            logger.error(error_msg)
            QMessageBox.critical(self, "Error", error_msg)
            
    def add_client_to_table(self, cliente):
        """Añade un cliente a la tabla"""
        row = self.clients_table.rowCount()
        self.clients_table.insertRow(row)
        
        # Formatear fecha de nacimiento
        fecha_nac = ""
        if cliente.get("fecha_nacimiento") and cliente["fecha_nacimiento"] != "0000-00-00":
            fecha = datetime.strptime(cliente["fecha_nacimiento"], "%Y-%m-%d")
            fecha_nac = fecha.strftime("%d/%m/%Y")
        
        # Añadir datos del cliente
        items = [
            QTableWidgetItem(str(cliente.get("id", ""))),
            QTableWidgetItem(cliente.get("nombres", "")),
            QTableWidgetItem(cliente["apellidos"]),
            QTableWidgetItem(cliente.get("tipo_documento", "DNI")),
            QTableWidgetItem(cliente.get("numero_documento", "")),
            QTableWidgetItem(fecha_nac),
            QTableWidgetItem(cliente.get("telefonos", "")),
            QTableWidgetItem(cliente.get("movil", "")),
            QTableWidgetItem(cliente.get("mail", "")),
            QTableWidgetItem(cliente.get("direccion", "")),
            QTableWidgetItem(cliente.get("localidad", ""))
        ]
        
        # Configurar items
        for col, item in enumerate(items):
            item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
            if col in [0, 3, 5]:  # ID, Tipo Doc y Fecha Nac centrados
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.clients_table.setItem(row, col, item)
    
    def on_selection_changed(self):
        """Maneja el cambio de selección en la tabla"""
        selected_rows = self.clients_table.selectedItems()
        has_selection = len(selected_rows) > 0
        
        # Activar/desactivar botones según la selección
        self.edit_button.setEnabled(has_selection)
        self.delete_button.setEnabled(has_selection)
    
    def get_selected_client_id(self):
        """Obtiene el ID del cliente seleccionado"""
        selected_rows = self.clients_table.selectedItems()
        if not selected_rows:
            return None
        # El ID está en la primera columna
        return selected_rows[0].text()
    
    def edit_selected_client(self):
        """Edita el cliente seleccionado"""
        client_id = self.get_selected_client_id()
        if client_id:
            self.show_edit_client_dialog(client_id)
    
    def delete_selected_client(self):
        """Elimina el cliente seleccionado"""
        client_id = self.get_selected_client_id()
        if client_id:
            self.delete_client(client_id)
    
    def show_add_client_dialog(self):
        """Muestra el diálogo para agregar un nuevo cliente"""
        dialog = ClienteDialog(parent=self, token=self.token)
        if dialog.exec() == dialog.DialogCode.Accepted:
            self.load_clients()

    def show_edit_client_dialog(self, client_id):
        """Muestra el diálogo para editar un cliente existente"""
        dialog = ClienteDialog(parent=self, client_id=client_id, token=self.token)
        if dialog.exec() == dialog.DialogCode.Accepted:
            self.load_clients()

    def delete_client(self, client_id):
        """Elimina un cliente"""
        reply = QMessageBox.question(
            self,
            "Confirmar eliminación",
            "¿Está seguro de que desea eliminar este cliente?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                response = requests.delete(
                    f"http://localhost:8000/api/v1/clientes/{client_id}",
                    headers={"Authorization": f"Bearer {self.token}"}
                )
                response.raise_for_status()
                self.load_clients()
                QMessageBox.information(self, "Éxito", "Cliente eliminado exitosamente")
            except requests.RequestException as e:
                QMessageBox.critical(self, "Error", f"Error al eliminar cliente: {str(e)}")
