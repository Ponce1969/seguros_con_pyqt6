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
        self.corredores_table.setColumnCount(10)  # Eliminada la columna de acciones
        self.corredores_table.setHorizontalHeaderLabels([
            "ID", "Número", "Nombres", "Apellidos", "Documento",
            "Teléfonos", "Móvil", "Email", "Dirección", "Localidad"
        ])
        
        # Configurar la tabla
        header = self.corredores_table.horizontalHeader()
        header.setStretchLastSection(True)
        for i in range(10):
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
        try:
            row = self.corredores_table.rowCount()
            self.corredores_table.insertRow(row)
            
            # Añadir datos del corredor - Usar 'numero' como ID
            items = [
                QTableWidgetItem(str(corredor.get("numero", ""))),  # Usamos 'numero' como ID
                QTableWidgetItem(str(corredor.get("numero", ""))),  # Número visible
                QTableWidgetItem(corredor.get("nombres", "")),
                QTableWidgetItem(corredor["apellidos"]),
                QTableWidgetItem(corredor.get("documento", "")),
                QTableWidgetItem(corredor.get("telefonos", "")),
                QTableWidgetItem(corredor.get("movil", "")),
                QTableWidgetItem(corredor.get("mail", "")),
                QTableWidgetItem(corredor.get("direccion", "")),
                QTableWidgetItem(corredor.get("localidad", ""))
            ]
            
            logger.debug(f"Agregando corredor a la tabla - ID/Número: {corredor.get('numero', '')}")
            
            # Configurar items
            for col, item in enumerate(items):
                if item is None:
                    logger.error(f"Item None encontrado en columna {col}")
                    continue
                    
                item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
                if col in [0, 1]:  # ID y Número centrados
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.corredores_table.setItem(row, col, item)
                
        except Exception as e:
            logger.error(f"Error al agregar corredor a la tabla: {str(e)}")

    def get_selected_corredor_id(self):
        """Obtiene el ID del corredor seleccionado"""
        try:
            current_row = self.corredores_table.currentRow()
            logger.debug(f"Fila seleccionada: {current_row}")
            
            if current_row == -1:
                logger.debug("No hay fila seleccionada")
                return None
                
            # El ID está en la primera columna
            id_item = self.corredores_table.item(current_row, 0)
            if id_item is None:
                logger.error(f"No se pudo obtener el item de la columna ID en la fila {current_row}")
                return None
                
            corredor_id = id_item.text()
            logger.debug(f"ID del corredor seleccionado: '{corredor_id}'")
            
            # Verificar si el ID es válido
            if not corredor_id.strip():
                logger.error("ID del corredor está vacío")
                return None
                
            return corredor_id
            
        except Exception as e:
            logger.error(f"Error al obtener ID del corredor: {str(e)}")
            return None
    
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
        try:
            logger.debug("Intentando eliminar corredor...")
            corredor_id = self.get_selected_corredor_id()
            
            if not corredor_id:
                logger.warning("No se pudo obtener el ID del corredor")
                QMessageBox.warning(self, "Advertencia", "Por favor, seleccione un corredor para eliminar")
                return
                
            logger.debug(f"Procediendo a eliminar corredor ID: {corredor_id}")
            self.delete_corredor(corredor_id)
            
        except Exception as e:
            error_msg = f"Error al eliminar corredor: {str(e)}"
            logger.error(error_msg)
            QMessageBox.critical(self, "Error", error_msg)
    
    def delete_corredor(self, corredor_id):
        """Elimina un corredor"""
        try:
            # Obtener el número del corredor para el mensaje
            row = None
            for i in range(self.corredores_table.rowCount()):
                if self.corredores_table.item(i, 0).text() == corredor_id:
                    row = i
                    break
            
            logger.debug(f"Fila encontrada para corredor ID {corredor_id}: {row}")
            
            if row is not None:
                corredor_numero = self.corredores_table.item(row, 1).text()
                mensaje = f"¿Está seguro de que desea eliminar el corredor número {corredor_numero}?"
            else:
                mensaje = "¿Está seguro de que desea eliminar este corredor?"
            
            reply = QMessageBox.question(
                self,
                "Confirmar eliminación",
                mensaje,
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                logger.debug(f"Enviando solicitud DELETE para corredor ID: {corredor_id}")
                response = requests.delete(
                    f"http://localhost:8000/api/v1/corredores/{corredor_id}",
                    headers={"Authorization": f"Bearer {self.token}"}
                )
                response.raise_for_status()
                
                logger.debug("Corredor eliminado exitosamente")
                self.load_corredores()
                QMessageBox.information(self, "Éxito", "Corredor eliminado exitosamente")
                
        except requests.RequestException as e:
            error_msg = f"Error al eliminar corredor: {str(e)}"
            logger.error(error_msg)
            QMessageBox.critical(self, "Error", error_msg)
        except Exception as e:
            error_msg = f"Error inesperado: {str(e)}"
            logger.error(error_msg)
            QMessageBox.critical(self, "Error", error_msg)
    
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
