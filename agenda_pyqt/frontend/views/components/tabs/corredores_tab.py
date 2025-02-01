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
        
        # Barra de herramientas
        toolbar = QHBoxLayout()
        toolbar.setSpacing(10)
        
        # Botones principales
        add_button = QPushButton("Agregar Corredor")
        add_button.setFixedWidth(120)
        add_button.clicked.connect(self.show_add_corredor_dialog)
        toolbar.addWidget(add_button)
        
        # Botones de acción (desactivados por defecto)
        self.edit_button = QPushButton("Editar")
        self.edit_button.setFixedWidth(80)
        self.edit_button.setEnabled(False)
        self.edit_button.clicked.connect(self.edit_selected_corredor)
        toolbar.addWidget(self.edit_button)
        
        self.delete_button = QPushButton("Eliminar")
        self.delete_button.setFixedWidth(80)
        self.delete_button.setEnabled(False)
        self.delete_button.clicked.connect(self.delete_selected_corredor)
        toolbar.addWidget(self.delete_button)
        
        refresh_button = QPushButton("Actualizar Lista")
        refresh_button.setFixedWidth(120)
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
        self.corredores_table.setColumnCount(9)  # Reducido en 1 por eliminar columna ID
        self.corredores_table.setHorizontalHeaderLabels([
            "N° Corredor", "Nombres", "Apellidos", "Documento",
            "Teléfonos", "Móvil", "Email", "Dirección", "Localidad"
        ])
        
        # Configurar la tabla
        header = self.corredores_table.horizontalHeader()
        header.setStretchLastSection(True)
        for i in range(9):
            header.setSectionResizeMode(i, header.ResizeMode.ResizeToContents)
        
        self.corredores_table.verticalHeader().setVisible(False)
        self.corredores_table.setAlternatingRowColors(True)
        self.corredores_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.corredores_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.corredores_table.setMinimumHeight(300)
        
        # Conectar evento de selección
        self.corredores_table.selectionModel().selectionChanged.connect(self.on_selection_changed)

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
            
            # Mostrar la estructura de los primeros corredores
            for i, corredor in enumerate(corredores[:2]):  # Solo mostrar los primeros 2 para no saturar los logs
                logger.debug(f"Estructura del corredor {i + 1}: {corredor}")
            
            self.corredores_table.setRowCount(0)
            
            if not corredores:
                logger.debug("No se encontraron corredores")
                self.corredores_table.setRowCount(1)
                empty_message = QTableWidgetItem("No hay corredores registrados")
                empty_message.setFlags(Qt.ItemFlag.ItemIsEnabled)
                empty_message.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.corredores_table.setSpan(0, 0, 1, 9)
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
        try:
            row = self.corredores_table.rowCount()
            self.corredores_table.insertRow(row)
            
            # Añadir datos del corredor
            items = [
                QTableWidgetItem(str(corredor.get("numero", ""))),  # Número de corredor
                QTableWidgetItem(corredor.get("nombres", "")),
                QTableWidgetItem(corredor["apellidos"]),
                QTableWidgetItem(corredor.get("documento", "")),
                QTableWidgetItem(corredor.get("telefonos", "")),
                QTableWidgetItem(corredor.get("movil", "")),
                QTableWidgetItem(corredor.get("mail", "")),
                QTableWidgetItem(corredor.get("direccion", "")),
                QTableWidgetItem(corredor.get("localidad", ""))
            ]
            
            logger.debug(f"Agregando corredor a la tabla - Número: {corredor.get('numero', '')}")
            
            # Configurar items
            for col, item in enumerate(items):
                if item is None:
                    logger.error(f"Item None encontrado en columna {col}")
                    continue
                    
                item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
                if col in [0]:  # Número centrado
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.corredores_table.setItem(row, col, item)
                
        except Exception as e:
            logger.error(f"Error al agregar corredor a la tabla: {str(e)}")

    def get_selected_corredor_id(self):
        """Obtiene el número del corredor seleccionado"""
        selected_items = self.corredores_table.selectedItems()
        if not selected_items:
            return None
        return self.corredores_table.item(selected_items[0].row(), 0).text()

    def on_selection_changed(self, selected, deselected):
        """Maneja el cambio de selección en la tabla"""
        try:
            current_row = self.corredores_table.currentRow()
            logger.debug(f"Cambio de selección - Fila actual: {current_row}")
            
            has_selection = current_row != -1
            self.edit_button.setEnabled(has_selection)
            self.delete_button.setEnabled(has_selection)
            
            if has_selection:
                corredor_id = self.get_selected_corredor_id()
                logger.debug(f"Corredor seleccionado - ID: {corredor_id}")
                
        except Exception as e:
            logger.error(f"Error en on_selection_changed: {str(e)}")
    
    def edit_selected_corredor(self):
        """Edita el corredor seleccionado"""
        try:
            corredor_id = self.get_selected_corredor_id()
            if not corredor_id:
                QMessageBox.warning(self, "Advertencia", "Por favor seleccione un corredor para editar")
                return
                
            logger.debug(f"Intentando editar corredor {corredor_id}")
            dialog = CorredorDialog(self, corredor_id=corredor_id, token=self.token)
            if dialog.exec() == dialog.DialogCode.Accepted:
                self.load_corredores()  # Recargar la tabla
                
        except Exception as e:
            error_msg = f"Error al editar corredor: {str(e)}"
            logger.error(error_msg)
            QMessageBox.critical(self, "Error", error_msg)
    
    def delete_selected_corredor(self):
        """Elimina el corredor seleccionado"""
        numero_corredor = self.get_selected_corredor_id()
        if not numero_corredor:
            return
        
        reply = QMessageBox.question(
            self,
            "Confirmar Eliminación",
            f"¿Está seguro que desea eliminar el corredor N° {numero_corredor}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.delete_corredor(numero_corredor)

    def delete_corredor(self, numero_corredor):
        """Elimina un corredor"""
        try:
            response = requests.delete(
                f"http://localhost:8000/api/v1/corredores/{numero_corredor}",
                headers={"Authorization": f"Bearer {self.token}"}
            )
            response.raise_for_status()
            self.load_corredores()
            QMessageBox.information(self, "Éxito", "Corredor eliminado exitosamente")
        except requests.RequestException as e:
            error_msg = f"Error al eliminar corredor: {str(e)}"
            logger.error(error_msg)
            QMessageBox.critical(self, "Error", error_msg)

    def show_add_corredor_dialog(self):
        """Muestra el diálogo para agregar un nuevo corredor"""
        dialog = CorredorDialog(parent=self, token=self.token)
        if dialog.exec() == dialog.DialogCode.Accepted:
            self.load_corredores()

    def show_edit_corredor_dialog(self, numero_corredor):
        """Muestra el diálogo para editar un corredor existente"""
        dialog = CorredorDialog(self, numero_corredor, self.token)
        if dialog.exec():
            self.load_corredores()  # Recargar la lista de corredores
