import requests
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QComboBox, QMessageBox, QTabWidget,
    QListWidget, QListWidgetItem, QSizePolicy, QLabel, QTableWidget, QTableWidgetItem, 
    QFormLayout, QLineEdit, QDateEdit, QTextEdit, QHeaderView, QDialog
)
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtGui import QIcon
from .views.cliente_form import ClienteForm
from .views.movimiento_form import MovimientoForm
from .views.corredor_form import CorredorForm

class MainWindow(QMainWindow):
    def __init__(self, cliente_api=None):
        super().__init__()
        self.cliente_api = cliente_api
        self.setWindowTitle("Gestión de Seguros")
        self.setup_ui()
        self.setup_connections()
        self.load_clientes()

    def setup_ui(self):
        # Widget principal
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # Crear el widget de pestañas
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)

        # Pestaña de Clientes
        cliente_tab = QWidget()
        cliente_layout = QVBoxLayout(cliente_tab)
        
        # Selector de cliente y botones
        selector_layout = QHBoxLayout()
        
        # Contenedor para el selector
        selector_container = QHBoxLayout()
        self.cliente_selector = QComboBox()
        self.cliente_selector.addItem("Nuevo Cliente")
        self.cliente_selector.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        selector_container.addWidget(self.cliente_selector)
        selector_layout.addLayout(selector_container, stretch=2)
        
        # Contenedor para los botones
        buttons_container = QHBoxLayout()
        self.nuevo_cliente_button = QPushButton("Nuevo")
        self.edit_button = QPushButton("Editar")
        self.submit_button = QPushButton("Guardar")
        self.delete_button = QPushButton("Eliminar")
        
        # Establecer un ancho fijo para todos los botones
        button_width = 100
        for button in [self.nuevo_cliente_button, self.edit_button, self.submit_button, self.delete_button]:
            button.setFixedWidth(button_width)
            buttons_container.addWidget(button)
        
        selector_layout.addLayout(buttons_container, stretch=3)
        cliente_layout.addLayout(selector_layout)
        
        # Formulario de cliente
        self.cliente_form = ClienteForm(cliente_api=self.cliente_api)
        cliente_layout.addWidget(self.cliente_form)
        
        self.tab_widget.addTab(cliente_tab, "Clientes")

        # Pestaña de Movimientos
        movimiento_tab = QWidget()
        movimiento_layout = QVBoxLayout(movimiento_tab)
        
        # Lista de movimientos
        self.movimientos_list = QListWidget()
        movimiento_layout.addWidget(self.movimientos_list)
        
        # Botones para la lista de movimientos
        list_buttons_layout = QHBoxLayout()
        self.nuevo_movimiento_button = QPushButton("Nuevo Movimiento")
        self.editar_movimiento_button = QPushButton("Editar")
        self.borrar_movimiento_button = QPushButton("Dar de Baja")
        list_buttons_layout.addWidget(self.nuevo_movimiento_button)
        list_buttons_layout.addWidget(self.editar_movimiento_button)
        list_buttons_layout.addWidget(self.borrar_movimiento_button)
        movimiento_layout.addLayout(list_buttons_layout)
        
        # Formulario de movimiento
        self.movimiento_form = MovimientoForm()
        movimiento_layout.addWidget(self.movimiento_form)
        
        # Botones para movimientos
        movimiento_buttons = QHBoxLayout()
        self.guardar_movimiento_button = QPushButton("Guardar Movimiento")
        self.cancelar_movimiento_button = QPushButton("Cancelar")
        movimiento_buttons.addWidget(self.guardar_movimiento_button)
        movimiento_buttons.addWidget(self.cancelar_movimiento_button)
        movimiento_layout.addLayout(movimiento_buttons)
        
        self.tab_widget.addTab(movimiento_tab, "Movimientos")

        # Pestaña de Corredores
        corredores_tab = QWidget()
        corredores_layout = QVBoxLayout(corredores_tab)
        
        # Formulario de corredor
        self.corredor_form = CorredorForm()
        corredores_layout.addWidget(self.corredor_form)
        
        # Botones para corredores
        corredores_buttons = QHBoxLayout()
        self.nuevo_corredor_button = QPushButton("Nuevo Corredor")
        self.guardar_corredor_button = QPushButton("Guardar Corredor")
        corredores_buttons.addWidget(self.nuevo_corredor_button)
        corredores_buttons.addWidget(self.guardar_corredor_button)
        corredores_layout.addLayout(corredores_buttons)
        
        self.tab_widget.addTab(corredores_tab, "Corredores")

    def setup_connections(self):
        self.cliente_selector.currentIndexChanged.connect(self.on_cliente_selected)
        self.nuevo_cliente_button.clicked.connect(self.nuevo_cliente)
        self.edit_button.clicked.connect(self.editar_cliente)
        self.submit_button.clicked.connect(self.submit_form)
        self.delete_button.clicked.connect(self.delete_cliente)
        
        self.nuevo_movimiento_button.clicked.connect(self.nuevo_movimiento)
        self.editar_movimiento_button.clicked.connect(self.editar_movimiento)
        self.borrar_movimiento_button.clicked.connect(self.borrar_movimiento)
        self.guardar_movimiento_button.clicked.connect(self.guardar_movimiento)
        self.cancelar_movimiento_button.clicked.connect(self.cancelar_movimiento)
        self.movimientos_list.itemClicked.connect(self.on_movimiento_selected)

        self.nuevo_corredor_button.clicked.connect(self.nuevo_corredor)
        self.guardar_corredor_button.clicked.connect(self.guardar_corredor)

    def load_clientes(self):
        try:
            if self.cliente_api:
                clientes = self.cliente_api.obtener_clientes()
                self.cliente_selector.clear()
                self.cliente_selector.addItem("Nuevo Cliente")
                for cliente in clientes:
                    self.cliente_selector.addItem(
                        f"{cliente['nombres']} {cliente['apellidos']}",
                        cliente
                    )
                # Cargar movimientos si hay un cliente seleccionado
                if self.cliente_selector.currentIndex() > 0:
                    self.load_movimientos()
            else:
                QMessageBox.warning(
                    self,
                    "Error",
                    "No se ha inicializado el cliente API"
                )
        except Exception as e:
            QMessageBox.warning(
                self,
                "Error",
                f"No se pudieron cargar los clientes del servidor: {str(e)}"
            )

    def load_movimientos(self):
        if self.cliente_selector.currentIndex() == 0:
            self.movimientos_list.clear()
            return
            
        try:
            cliente = self.cliente_selector.currentData()
            if self.cliente_api:
                movimientos = self.cliente_api.obtener_movimientos_cliente(cliente["id"])
                
                self.movimientos_list.clear()
                
                movimientos_activos = [m for m in movimientos if not m.get('activo', False)]
                
                if movimientos_activos:
                    for movimiento in movimientos_activos:
                        try:
                            # Formatear el texto del movimiento con mejor manejo de datos
                            fecha = movimiento.get('fecha_mov', 'Sin fecha')
                            poliza = movimiento.get('poliza', 'Sin póliza')
                            premio = movimiento.get('premio', 0)
                            moneda = movimiento.get('moneda', '$')
                            tipo_seguro = movimiento.get('tipo_seguro', 'No especificado')
                            observaciones = movimiento.get('observaciones', '').split('\r\n')[0]  # Primera línea
                            
                            texto = (
                                f"Fecha: {fecha} | "
                                f"Póliza: {poliza} | "
                                f"Tipo: {tipo_seguro} | "
                                f"Premio: {moneda} {premio:,.2f}"
                            )
                            if observaciones:
                                texto += f" | {observaciones}"
                                
                            item = QListWidgetItem(texto)
                            item.setData(Qt.ItemDataRole.UserRole, movimiento)
                            self.movimientos_list.addItem(item)
                        except (KeyError, ValueError) as e:
                            print(f"Error al procesar movimiento: {str(e)}")
                            continue
                else:
                    item = QListWidgetItem("No hay movimientos activos para este cliente")
                    self.movimientos_list.addItem(item)
            else:
                QMessageBox.warning(
                    self,
                    "Error",
                    "No se ha inicializado el cliente API"
                )
        except Exception as e:
            QMessageBox.warning(
                self,
                "Error",
                f"Error al cargar los movimientos: {str(e)}"
            )

    def nuevo_movimiento(self):
        if self.cliente_selector.currentIndex() == 0:
            QMessageBox.warning(self, "Error", "Debe seleccionar un cliente primero")
            return
        self.movimiento_form.clear_form()
        self.movimiento_form.setEnabled(True)

    def editar_movimiento(self):
        item = self.movimientos_list.currentItem()
        if item is None:
            QMessageBox.warning(self, "Error", "Debe seleccionar un movimiento para editar")
            return
        
        movimiento = item.data(Qt.ItemDataRole.UserRole)
        if movimiento is None:
            QMessageBox.warning(self, "Error", "El movimiento seleccionado no tiene datos asociados")
            return
            
        self.movimiento_form.set_form_data(movimiento)
        self.movimiento_form.setEnabled(True)

    def borrar_movimiento(self):
        item = self.movimientos_list.currentItem()
        if item is None:
            QMessageBox.warning(self, "Error", "Debe seleccionar un movimiento para dar de baja")
            return
        
        movimiento = item.data(Qt.ItemDataRole.UserRole)
        if movimiento is None:
            QMessageBox.warning(self, "Error", "El movimiento seleccionado no tiene datos asociados")
            return
        
        # Verificar ID del movimiento
        movimiento_id = movimiento.get('id_movimiento')
        if not movimiento_id:
            QMessageBox.warning(self, "Error", "El movimiento no tiene un ID válido")
            return
        
        reply = QMessageBox.question(
            self,
            'Confirmar Baja',
            '¿Está seguro de que desea eliminar este seguro?\nEsta acción no se puede deshacer.',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                if self.cliente_api:
                    self.cliente_api.eliminar_movimiento(movimiento_id)
                    
                    # Remover el item de la lista inmediatamente
                    row = self.movimientos_list.row(item)
                    self.movimientos_list.takeItem(row)
                    
                    # Si no quedan items, mostrar mensaje
                    if self.movimientos_list.count() == 0:
                        self.movimientos_list.addItem("No hay movimientos activos para este cliente")
                    
                    QMessageBox.information(self, "Éxito", "Seguro eliminado exitosamente")
                    self.movimiento_form.clear_form()
                else:
                    QMessageBox.warning(
                        self,
                        "Error",
                        "No se ha inicializado el cliente API"
                    )
            except Exception as e:
                QMessageBox.warning(
                    self,
                    "Error",
                    f"Error al eliminar el seguro: {str(e)}"
                )

    def cancelar_movimiento(self):
        self.movimiento_form.clear_form()
        self.movimientos_list.clearSelection()

    def on_movimiento_selected(self, item):
        movimiento = item.data(Qt.ItemDataRole.UserRole)
        self.movimiento_form.set_form_data(movimiento)
        self.movimiento_form.setEnabled(False)  # Deshabilitar edición hasta que se presione "Editar"

    def on_cliente_selected(self, index):
        if index == 0:  # Nuevo Cliente
            self.cliente_form.clear_form()
            self.edit_button.setEnabled(False)
            self.delete_button.setEnabled(False)
            self.submit_button.setEnabled(True)
        else:
            cliente = self.cliente_selector.currentData()
            if cliente:
                self.cliente_form.set_form_data(cliente)
                self.edit_button.setEnabled(True)
                self.delete_button.setEnabled(True)
                self.submit_button.setEnabled(False)
                self.load_movimientos()  # Cargar movimientos del cliente seleccionado

    def nuevo_cliente(self):
        self.cliente_selector.setCurrentIndex(0)
        self.cliente_form.clear_form()
        self.edit_button.setEnabled(False)
        self.delete_button.setEnabled(False)
        self.submit_button.setEnabled(True)

    def editar_cliente(self):
        self.cliente_form.setEnabled(True)
        self.submit_button.setEnabled(True)
        self.edit_button.setEnabled(False)

    def submit_form(self):
        try:
            if not self.cliente_api:
                QMessageBox.warning(self, "Error", "No se ha inicializado el cliente API")
                return
                
            data = self.cliente_form.get_form_data()
            
            if self.cliente_selector.currentIndex() == 0:
                # Crear nuevo cliente
                cliente = self.cliente_api.crear_cliente(data)
                QMessageBox.information(self, "Éxito", "Cliente creado exitosamente")
                self.load_clientes()
                # Seleccionar el cliente recién creado
                self.cliente_selector.setCurrentIndex(self.cliente_selector.count() - 1)
            else:
                # Actualizar cliente existente
                cliente = self.cliente_selector.currentData()
                cliente_actualizado = self.cliente_api.actualizar_cliente(cliente["id"], data)
                QMessageBox.information(self, "Éxito", "Cliente actualizado exitosamente")
                self.load_clientes()
                # Mantener seleccionado el cliente editado
                for i in range(self.cliente_selector.count()):
                    item_data = self.cliente_selector.itemData(i)
                    if item_data and item_data.get('id') == cliente['id']:
                        self.cliente_selector.setCurrentIndex(i)
                        break
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al procesar el formulario: {str(e)}")

    def delete_cliente(self):
        if self.cliente_selector.currentIndex() == 0:
            return
        
        if not self.cliente_api:
            QMessageBox.warning(self, "Error", "No se ha inicializado el cliente API")
            return
        
        reply = QMessageBox.question(
            self,
            'Confirmar Eliminación',
            '¿Está seguro de que desea eliminar este cliente?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                cliente = self.cliente_selector.currentData()
                self.cliente_api.eliminar_cliente(cliente["id"])
                QMessageBox.information(self, "Éxito", "Cliente eliminado exitosamente")
                current_index = self.cliente_selector.currentIndex()
                self.load_clientes()
                # Seleccionar el siguiente cliente o "Nuevo Cliente" si no hay más
                if self.cliente_selector.count() > 1:
                    self.cliente_selector.setCurrentIndex(min(current_index, self.cliente_selector.count() - 1))
                else:
                    self.cliente_selector.setCurrentIndex(0)
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Error al eliminar cliente: {str(e)}")

    def guardar_movimiento(self):
        if self.cliente_selector.currentIndex() == 0:
            QMessageBox.warning(self, "Error", "Debe seleccionar un cliente primero")
            return
            
        if not self.cliente_api:
            QMessageBox.warning(self, "Error", "No se ha inicializado el cliente API")
            return
            
        try:
            cliente = self.cliente_selector.currentData()
            data = self.movimiento_form.get_form_data()
            
            # Validar datos requeridos
            required_fields = ['fecha_mov', 'premio', 'moneda']
            missing_fields = [field for field in required_fields if not data.get(field)]
            
            if missing_fields:
                QMessageBox.warning(
                    self,
                    "Error de Validación",
                    f"Los siguientes campos son requeridos: {', '.join(missing_fields)}"
                )
                return
                
            data['cliente_id'] = cliente['id']
            
            movimiento = self.cliente_api.crear_movimiento(cliente['id'], data)
            QMessageBox.information(self, "Éxito", "Movimiento guardado exitosamente")
            self.movimiento_form.clear_form()
            self.load_movimientos()
        except Exception as e:
            QMessageBox.warning(
                self,
                "Error",
                f"Error al guardar el movimiento: {str(e)}"
            )

    def nuevo_corredor(self):
        self.corredor_form.clear_form()
        self.corredor_form.setEnabled(True)

    def guardar_corredor(self):
        try:
            if not self.cliente_api:
                QMessageBox.warning(self, "Error", "No se ha inicializado el cliente API")
                return
                
            data = self.corredor_form.get_form_data()
            
            # Crear nuevo corredor
            corredor = self.cliente_api.crear_corredor(data)
            QMessageBox.information(self, "Éxito", "Corredor creado exitosamente")
            self.corredor_form.clear_form()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al procesar el formulario: {str(e)}")