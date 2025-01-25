from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                            QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView)
from PyQt6.QtCore import Qt, QDate
from ..dialogs.movimiento_dialog import MovimientoDialog
import requests
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class MovimientosTab(QWidget):
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
        add_button = QPushButton("Agregar Movimiento")
        add_button.setFixedWidth(140)
        add_button.clicked.connect(self.show_add_movement_dialog)
        toolbar.addWidget(add_button)
        
        # Botones de acción (desactivados por defecto)
        self.edit_button = QPushButton("Editar")
        self.edit_button.setFixedWidth(80)
        self.edit_button.setEnabled(False)
        self.edit_button.clicked.connect(self.edit_selected_movement)
        toolbar.addWidget(self.edit_button)
        
        self.delete_button = QPushButton("Eliminar")
        self.delete_button.setFixedWidth(80)
        self.delete_button.setEnabled(False)
        self.delete_button.clicked.connect(self.delete_selected_movement)
        toolbar.addWidget(self.delete_button)
        
        refresh_button = QPushButton("Actualizar Lista")
        refresh_button.setFixedWidth(120)
        refresh_button.clicked.connect(self.load_movements)
        toolbar.addWidget(refresh_button)
        
        toolbar.addStretch()
        layout.addLayout(toolbar)
        
        # Tabla de movimientos
        self.setup_table()
        layout.addWidget(self.movements_table)
        
        # Cargar movimientos
        self.load_movements()
        
    def setup_table(self):
        """Configura la tabla de movimientos"""
        self.movements_table = QTableWidget()
        self.movements_table.setColumnCount(13)
        self.movements_table.setHorizontalHeaderLabels([
            "ID", "Fecha Mov.", "Corredor", "Cliente",
            "Tipo Seguro", "Carpeta", "Póliza", "Endoso",
            "Vto. Desde", "Vto. Hasta", "Moneda", "Premio",
            "Cuotas"
        ])
        
        # Configurar la tabla
        header = self.movements_table.horizontalHeader()
        header.setStretchLastSection(True)
        for i in range(13):
            header.setSectionResizeMode(i, header.ResizeMode.ResizeToContents)
        
        self.movements_table.verticalHeader().setVisible(False)
        self.movements_table.setAlternatingRowColors(True)
        self.movements_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.movements_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.movements_table.setMinimumHeight(300)
        
        # Conectar evento de selección
        self.movements_table.itemSelectionChanged.connect(self.on_selection_changed)
        
    def load_movements(self):
        """Carga los movimientos desde la API"""
        try:
            logger.debug("Intentando cargar movimientos...")
            response = requests.get(
                "http://localhost:8000/api/v1/movimientos/",
                headers={"Authorization": f"Bearer {self.token}"}
            )
            logger.debug(f"Respuesta del servidor: {response.status_code}")
            
            response.raise_for_status()
            movimientos = response.json()
            logger.debug(f"Movimientos cargados: {len(movimientos)}")
            
            self.movements_table.setRowCount(0)
            
            if not movimientos:
                logger.debug("No se encontraron movimientos")
                self.movements_table.setRowCount(1)
                empty_message = QTableWidgetItem("No hay movimientos registrados")
                empty_message.setFlags(Qt.ItemFlag.ItemIsEnabled)
                empty_message.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.movements_table.setSpan(0, 0, 1, 13)
                self.movements_table.setItem(0, 0, empty_message)
                return
            
            for movimiento in movimientos:
                self.add_movement_to_table(movimiento)
            
            # Ajustar el tamaño de las filas
            self.movements_table.resizeRowsToContents()
            logger.debug("Tabla de movimientos actualizada exitosamente")
                
        except requests.RequestException as e:
            error_msg = f"Error al cargar movimientos: {str(e)}"
            logger.error(error_msg)
            QMessageBox.critical(self, "Error", error_msg)
            
    def add_movement_to_table(self, movimiento):
        """Añade un movimiento a la tabla"""
        row = self.movements_table.rowCount()
        self.movements_table.insertRow(row)
        
        # Formatear fechas
        fecha_mov = datetime.strptime(movimiento["FechaMov"], "%Y-%m-%d")
        fecha_mov_str = fecha_mov.strftime("%d/%m/%Y")
        
        fecha_desde = datetime.strptime(movimiento["Vto_Desde"], "%Y-%m-%d")
        fecha_desde_str = fecha_desde.strftime("%d/%m/%Y")
        
        fecha_hasta = datetime.strptime(movimiento["Vto_Hasta"], "%Y-%m-%d")
        fecha_hasta_str = fecha_hasta.strftime("%d/%m/%Y")
        
        # Formatear premio
        premio = float(movimiento["Premio"])
        premio_str = f"{premio:,.2f}"
        
        # Añadir datos del movimiento
        items = [
            QTableWidgetItem(str(movimiento["Id_movimiento"])),
            QTableWidgetItem(fecha_mov_str),
            QTableWidgetItem(str(movimiento["Corredor"])),
            QTableWidgetItem(movimiento["Cliente_nombre"]),
            QTableWidgetItem(str(movimiento["Tipo_seguro"])),
            QTableWidgetItem(movimiento.get("Carpeta", "")),
            QTableWidgetItem(movimiento["Poliza"]),
            QTableWidgetItem(movimiento.get("Endoso", "")),
            QTableWidgetItem(fecha_desde_str),
            QTableWidgetItem(fecha_hasta_str),
            QTableWidgetItem(movimiento.get("Moneda", "$")),
            QTableWidgetItem(premio_str),
            QTableWidgetItem(str(movimiento["Cuotas"]))
        ]
        
        # Configurar items
        for col, item in enumerate(items):
            item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
            if col in [0, 1, 8, 9]:  # ID y fechas centrados
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            elif col in [11]:  # Premio alineado a la derecha
                item.setTextAlignment(Qt.AlignmentFlag.AlignRight)
            self.movements_table.setItem(row, col, item)
    
    def on_selection_changed(self):
        """Maneja el cambio de selección en la tabla"""
        selected_rows = self.movements_table.selectedItems()
        has_selection = len(selected_rows) > 0
        
        # Activar/desactivar botones según la selección
        self.edit_button.setEnabled(has_selection)
        self.delete_button.setEnabled(has_selection)
    
    def get_selected_movement_id(self):
        """Obtiene el ID del movimiento seleccionado"""
        selected_rows = self.movements_table.selectedItems()
        if not selected_rows:
            return None
        # El ID está en la primera columna
        return selected_rows[0].text()
    
    def edit_selected_movement(self):
        """Edita el movimiento seleccionado"""
        movement_id = self.get_selected_movement_id()
        if movement_id:
            self.show_edit_movement_dialog(movement_id)
    
    def delete_selected_movement(self):
        """Elimina el movimiento seleccionado"""
        movement_id = self.get_selected_movement_id()
        if movement_id:
            self.delete_movement(movement_id)

    def show_add_movement_dialog(self):
        """Muestra el diálogo para agregar un nuevo movimiento"""
        dialog = MovimientoDialog(parent=self, token=self.token)
        if dialog.exec() == dialog.DialogCode.Accepted:
            self.load_movements()

    def show_edit_movement_dialog(self, movement_id):
        """Muestra el diálogo para editar un movimiento existente"""
        dialog = MovimientoDialog(parent=self, movement_id=movement_id, token=self.token)
        if dialog.exec() == dialog.DialogCode.Accepted:
            self.load_movements()

    def delete_movement(self, movement_id):
        """Elimina un movimiento"""
        reply = QMessageBox.question(
            self,
            "Confirmar eliminación",
            "¿Está seguro de que desea eliminar este movimiento?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                response = requests.delete(
                    f"http://localhost:8000/api/v1/movimientos/{movement_id}",
                    headers={"Authorization": f"Bearer {self.token}"}
                )
                response.raise_for_status()
                self.load_movements()
                QMessageBox.information(self, "Éxito", "Movimiento eliminado exitosamente")
            except requests.RequestException as e:
                QMessageBox.critical(self, "Error", f"Error al eliminar movimiento: {str(e)}")
