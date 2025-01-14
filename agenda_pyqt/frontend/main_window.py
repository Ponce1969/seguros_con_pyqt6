from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QLabel, QPushButton, QTableWidget, QTableWidgetItem,
                            QMessageBox, QDialog, QFormLayout, QLineEdit, QDateEdit,
                            QComboBox, QTextEdit, QSizePolicy, QHeaderView, QTabWidget)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QScreen
import requests
from datetime import datetime
from PyQt6.QtWidgets import QApplication

class MainWindow(QMainWindow):
    def __init__(self, token):
        super().__init__()
        self.token = token
        self.setWindowTitle("Sistema de Seguros")
        
        # Configurar tamaño inicial y política de redimensionamiento
        self.resize(1000, 600)
        self.setMinimumSize(800, 500)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Crear el widget de pestañas
        self.tab_widget = QTabWidget()
        
        # Pestaña de Clientes
        self.clients_tab = QWidget()
        self.setup_clients_tab()
        self.tab_widget.addTab(self.clients_tab, "Clientes")
        
        # Pestaña de Movimientos
        self.movements_tab = QWidget()
        self.setup_movements_tab()
        self.tab_widget.addTab(self.movements_tab, "Movimientos")
        
        # Pestaña de Corredores
        self.corredores_tab = QWidget()
        self.setup_corredores_tab()
        self.tab_widget.addTab(self.corredores_tab, "Corredores")
        
        layout.addWidget(self.tab_widget)
        
        # Centrar la ventana
        self.center_window()
    
    def setup_clients_tab(self):
        """Configura la pestaña de clientes"""
        layout = QVBoxLayout(self.clients_tab)
        layout.setContentsMargins(0, 10, 0, 0)
        
        # Barra de herramientas
        toolbar = QHBoxLayout()
        toolbar.setSpacing(10)
        
        add_button = QPushButton("Agregar Cliente")
        add_button.setFixedWidth(120)
        add_button.clicked.connect(self.show_add_client_dialog)
        toolbar.addWidget(add_button)
        
        refresh_button = QPushButton("Actualizar")
        refresh_button.setFixedWidth(120)
        refresh_button.clicked.connect(self.load_clients)
        toolbar.addWidget(refresh_button)
        
        toolbar.addStretch()
        layout.addLayout(toolbar)
        
        # Tabla de clientes
        self.clients_table = QTableWidget()
        self.clients_table.setColumnCount(10)
        self.clients_table.setHorizontalHeaderLabels([
            "ID", "Nombres", "Apellidos", "Documento",
            "Teléfonos", "Móvil", "Mail", "Dirección",
            "Localidad", "Acciones"
        ])
        
        self.clients_table.horizontalHeader().setStretchLastSection(True)
        self.clients_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.clients_table.verticalHeader().setVisible(False)
        self.clients_table.setAlternatingRowColors(True)
        
        layout.addWidget(self.clients_table)
        
        # Cargar clientes
        self.load_clients()
    
    def setup_movements_tab(self):
        """Configura la pestaña de movimientos"""
        layout = QVBoxLayout(self.movements_tab)
        layout.setContentsMargins(0, 10, 0, 0)
        
        # Barra de herramientas
        toolbar = QHBoxLayout()
        toolbar.setSpacing(10)
        
        add_button = QPushButton("Agregar Movimiento")
        add_button.setFixedWidth(150)
        add_button.clicked.connect(self.show_add_movement_dialog)
        toolbar.addWidget(add_button)
        
        refresh_button = QPushButton("Actualizar")
        refresh_button.setFixedWidth(120)
        refresh_button.clicked.connect(self.load_movements)
        toolbar.addWidget(refresh_button)
        
        toolbar.addStretch()
        layout.addLayout(toolbar)
        
        # Tabla de movimientos
        self.movements_table = QTableWidget()
        self.movements_table.setColumnCount(12)
        self.movements_table.setHorizontalHeaderLabels([
            "ID", "Cliente", "Fecha Mov.", "Corredor",
            "Tipo Seguro", "Carpeta", "Póliza", "Endoso",
            "Vigencia Desde", "Vigencia Hasta", "Premio", "Acciones"
        ])
        
        self.movements_table.horizontalHeader().setStretchLastSection(True)
        self.movements_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.movements_table.verticalHeader().setVisible(False)
        self.movements_table.setAlternatingRowColors(True)
        
        layout.addWidget(self.movements_table)
        
        # Cargar movimientos
        self.load_movements()
    
    def setup_corredores_tab(self):
        """Configura la pestaña de corredores"""
        layout = QVBoxLayout(self.corredores_tab)
        layout.setContentsMargins(0, 10, 0, 0)
        
        # Barra de herramientas
        toolbar = QHBoxLayout()
        toolbar.setSpacing(10)
        
        add_button = QPushButton("Agregar Corredor")
        add_button.setFixedWidth(120)
        add_button.clicked.connect(self.show_add_corredor_dialog)
        toolbar.addWidget(add_button)
        
        refresh_button = QPushButton("Actualizar")
        refresh_button.setFixedWidth(120)
        refresh_button.clicked.connect(self.load_corredores)
        toolbar.addWidget(refresh_button)
        
        toolbar.addStretch()
        layout.addLayout(toolbar)
        
        # Tabla de corredores
        self.corredores_table = QTableWidget()
        self.corredores_table.setColumnCount(5)
        self.corredores_table.setHorizontalHeaderLabels([
            "ID", "Nombre", "Apellido", "Teléfono", "Acciones"
        ])
        
        self.corredores_table.horizontalHeader().setStretchLastSection(True)
        self.corredores_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.corredores_table.verticalHeader().setVisible(False)
        self.corredores_table.setAlternatingRowColors(True)
        
        layout.addWidget(self.corredores_table)
        
        # Cargar corredores
        self.load_corredores()
    
    def center_window(self):
        """Centra la ventana en la pantalla"""
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        
        window_geometry = self.frameGeometry()
        center_point = screen_geometry.center()
        
        window_geometry.moveCenter(center_point)
        self.move(window_geometry.topLeft())
    
    def load_clients(self):
        """Carga la lista de clientes desde el servidor"""
        try:
            response = requests.get(
                'http://localhost:8000/clients/',
                headers={'Authorization': f'Bearer {self.token}'}
            )
            response.raise_for_status()
            clients = response.json()

            # Configurar la tabla
            self.clients_table.setRowCount(0)
            self.clients_table.setColumnCount(10)
            self.clients_table.setHorizontalHeaderLabels([
                "ID", "Nombres", "Apellidos", "Documento",
                "Teléfonos", "Móvil", "Mail", "Dirección",
                "Localidad", "Acciones"
            ])

            # Ajustar el ancho de las columnas
            header = self.clients_table.horizontalHeader()
            for i in range(self.clients_table.columnCount() - 1):  # -1 para excluir la columna de acciones
                header.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
            header.setSectionResizeMode(self.clients_table.columnCount() - 1, QHeaderView.ResizeMode.Fixed)

            # Llenar la tabla con los datos
            for row, client in enumerate(clients):
                self.clients_table.insertRow(row)
                self.clients_table.setItem(row, 0, QTableWidgetItem(client["id"]))
                self.clients_table.setItem(row, 1, QTableWidgetItem(client["nombres"]))
                self.clients_table.setItem(row, 2, QTableWidgetItem(client["apellidos"]))
                self.clients_table.setItem(row, 3, QTableWidgetItem(client["documento"]))
                self.clients_table.setItem(row, 4, QTableWidgetItem(client["telefonos"]))
                self.clients_table.setItem(row, 5, QTableWidgetItem(client["movil"]))
                self.clients_table.setItem(row, 6, QTableWidgetItem(client["mail"]))
                self.clients_table.setItem(row, 7, QTableWidgetItem(client["direccion"]))
                self.clients_table.setItem(row, 8, QTableWidgetItem(client["localidad"]))
                
                # Botones de acción
                action_widget = QWidget()
                action_layout = QHBoxLayout(action_widget)
                action_layout.setContentsMargins(0, 0, 0, 0)
                
                edit_button = QPushButton("Editar")
                edit_button.clicked.connect(lambda checked, cid=client["id"]: self.show_edit_client_dialog(cid))
                action_layout.addWidget(edit_button)
                
                delete_button = QPushButton("Eliminar")
                delete_button.clicked.connect(lambda checked, cid=client["id"]: self.delete_client(cid))
                action_layout.addWidget(delete_button)
                
                self.clients_table.setCellWidget(row, 9, action_widget)
            
            if response.status_code == 404:
                self.clients_table.setRowCount(1)
                empty_message = QTableWidgetItem("No hay clientes registrados. Use el botón 'Agregar Cliente' para comenzar.")
                empty_message.setFlags(Qt.ItemFlag.ItemIsEnabled)  # Hacer la celda de solo lectura
                self.clients_table.setSpan(0, 0, 1, 10)  # Combinar todas las columnas
                self.clients_table.setItem(0, 0, empty_message)
            
            else:
                QMessageBox.warning(
                    self,
                    "Error",
                    "No se pudieron cargar los clientes. Por favor, intente nuevamente."
                )
        
        except requests.RequestException as e:
            QMessageBox.warning(
                self,
                "Error de conexión",
                "No se pudo conectar con el servidor. Por favor, verifique que el servidor esté funcionando."
            )
        except Exception as e:
            QMessageBox.warning(
                self,
                "Error",
                f"Error al cargar los clientes: {str(e)}"
            )
    
    def load_movements(self):
        """Carga la lista de movimientos desde el servidor"""
        try:
            response = requests.get(
                "http://localhost:8000/movements",
                headers={"Authorization": f"Bearer {self.token}"}
            )
            
            # Limpiar la tabla
            self.movements_table.setRowCount(0)
            
            if response.status_code == 200:
                movements = response.json()
                if not movements:  # Si la lista está vacía
                    self.movements_table.setRowCount(1)
                    empty_message = QTableWidgetItem("No hay movimientos registrados. Use el botón 'Agregar Movimiento' para comenzar.")
                    empty_message.setFlags(Qt.ItemFlag.ItemIsEnabled)  # Hacer la celda de solo lectura
                    self.movements_table.setSpan(0, 0, 1, 12)  # Combinar todas las columnas
                    self.movements_table.setItem(0, 0, empty_message)
                    return
                
                for movement in movements:
                    row = self.movements_table.rowCount()
                    self.movements_table.insertRow(row)
                    
                    # Añadir datos del movimiento
                    self.movements_table.setItem(row, 0, QTableWidgetItem(str(movement["Id_movimiento"])))
                    self.movements_table.setItem(row, 1, QTableWidgetItem(str(movement["Cliente"])))
                    self.movements_table.setItem(row, 2, QTableWidgetItem(movement["FechaMov"]))
                    self.movements_table.setItem(row, 3, QTableWidgetItem(str(movement["Corredor"])))
                    self.movements_table.setItem(row, 4, QTableWidgetItem(str(movement["Tipo_seguro"])))
                    self.movements_table.setItem(row, 5, QTableWidgetItem(movement["Carpeta"]))
                    self.movements_table.setItem(row, 6, QTableWidgetItem(movement["Poliza"] or ""))
                    self.movements_table.setItem(row, 7, QTableWidgetItem(movement["Endoso"] or ""))
                    self.movements_table.setItem(row, 8, QTableWidgetItem(movement["Vto_Desde"]))
                    self.movements_table.setItem(row, 9, QTableWidgetItem(movement["Vto_Hasta"]))
                    self.movements_table.setItem(row, 10, QTableWidgetItem(str(movement["Premio"] or "")))
                    
                    # Botones de acción
                    action_widget = QWidget()
                    action_layout = QHBoxLayout(action_widget)
                    action_layout.setContentsMargins(0, 0, 0, 0)
                    
                    edit_button = QPushButton("Editar")
                    edit_button.clicked.connect(lambda checked, mid=movement["Id_movimiento"]: self.show_edit_movement_dialog(mid))
                    action_layout.addWidget(edit_button)
                    
                    delete_button = QPushButton("Eliminar")
                    delete_button.clicked.connect(lambda checked, mid=movement["Id_movimiento"]: self.delete_movement(mid))
                    action_layout.addWidget(delete_button)
                    
                    self.movements_table.setCellWidget(row, 11, action_widget)
            
            elif response.status_code == 404:
                self.movements_table.setRowCount(1)
                empty_message = QTableWidgetItem("No hay movimientos registrados. Use el botón 'Agregar Movimiento' para comenzar.")
                empty_message.setFlags(Qt.ItemFlag.ItemIsEnabled)  # Hacer la celda de solo lectura
                self.movements_table.setSpan(0, 0, 1, 12)  # Combinar todas las columnas
                self.movements_table.setItem(0, 0, empty_message)
            
            else:
                QMessageBox.warning(
                    self,
                    "Error",
                    f"No se pudieron cargar los movimientos. Código de error: {response.status_code}"
                )
        
        except requests.RequestException as e:
            QMessageBox.warning(
                self,
                "Error de conexión",
                "No se pudo conectar con el servidor. Por favor, verifique que el servidor esté funcionando."
            )
        except Exception as e:
            QMessageBox.warning(
                self,
                "Error",
                f"Error al cargar los movimientos: {str(e)}"
            )
    
    def load_corredores(self):
        """Carga la lista de corredores desde el servidor"""
        try:
            response = requests.get(
                "http://localhost:8000/corredores",
                headers={"Authorization": f"Bearer {self.token}"}
            )
            
            # Limpiar la tabla
            self.corredores_table.setRowCount(0)
            
            if response.status_code == 200:
                corredores = response.json()
                if not corredores:  # Si la lista está vacía
                    self.corredores_table.setRowCount(1)
                    empty_message = QTableWidgetItem("No hay corredores registrados. Use el botón 'Agregar Corredor' para comenzar.")
                    empty_message.setFlags(Qt.ItemFlag.ItemIsEnabled)  # Hacer la celda de solo lectura
                    self.corredores_table.setSpan(0, 0, 1, 5)  # Combinar todas las columnas
                    self.corredores_table.setItem(0, 0, empty_message)
                    return
                
                for corredor in corredores:
                    row = self.corredores_table.rowCount()
                    self.corredores_table.insertRow(row)
                    
                    # Añadir datos del corredor
                    self.corredores_table.setItem(row, 0, QTableWidgetItem(str(corredor["id"])))
                    self.corredores_table.setItem(row, 1, QTableWidgetItem(corredor["nombre"]))
                    self.corredores_table.setItem(row, 2, QTableWidgetItem(corredor["apellido"]))
                    self.corredores_table.setItem(row, 3, QTableWidgetItem(corredor["telefono"]))
                    
                    # Botones de acción
                    action_widget = QWidget()
                    action_layout = QHBoxLayout(action_widget)
                    action_layout.setContentsMargins(0, 0, 0, 0)
                    
                    edit_button = QPushButton("Editar")
                    edit_button.clicked.connect(lambda checked, cid=corredor["id"]: self.show_edit_corredor_dialog(cid))
                    action_layout.addWidget(edit_button)
                    
                    delete_button = QPushButton("Eliminar")
                    delete_button.clicked.connect(lambda checked, cid=corredor["id"]: self.delete_corredor(cid))
                    action_layout.addWidget(delete_button)
                    
                    self.corredores_table.setCellWidget(row, 4, action_widget)
            
            elif response.status_code == 404:
                self.corredores_table.setRowCount(1)
                empty_message = QTableWidgetItem("No hay corredores registrados. Use el botón 'Agregar Corredor' para comenzar.")
                empty_message.setFlags(Qt.ItemFlag.ItemIsEnabled)  # Hacer la celda de solo lectura
                self.corredores_table.setSpan(0, 0, 1, 5)  # Combinar todas las columnas
                self.corredores_table.setItem(0, 0, empty_message)
            
            else:
                QMessageBox.warning(
                    self,
                    "Error",
                    f"No se pudieron cargar los corredores. Código de error: {response.status_code}"
                )
        
        except requests.RequestException as e:
            QMessageBox.warning(
                self,
                "Error de conexión",
                "No se pudo conectar con el servidor. Por favor, verifique que el servidor esté funcionando."
            )
        except Exception as e:
            QMessageBox.warning(
                self,
                "Error",
                f"Error al cargar los corredores: {str(e)}"
            )
    
    def show_add_client_dialog(self):
        """Muestra el diálogo para agregar un nuevo cliente"""
        dialog = ClientDialog(self.token, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_clients()
    
    def show_edit_client_dialog(self, client_id):
        """Muestra el diálogo para editar un cliente existente"""
        dialog = ClientDialog(self.token, client_id=client_id, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
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
                    f"http://localhost:8000/clients/{client_id}",
                    headers={"Authorization": f"Bearer {self.token}"}
                )
                
                if response.status_code == 200:
                    QMessageBox.information(self, "Éxito", "Cliente eliminado correctamente")
                    self.load_clients()
                else:
                    QMessageBox.warning(self, "Error", "No se pudo eliminar el cliente")
            
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al eliminar cliente: {str(e)}")

    def show_add_movement_dialog(self):
        """Muestra el diálogo para agregar un nuevo movimiento"""
        dialog = MovementDialog(self.token, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_movements()

    def show_edit_movement_dialog(self, movement_id):
        """Muestra el diálogo para editar un movimiento existente"""
        dialog = MovementDialog(self.token, movement_id=movement_id, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
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
                    f"http://localhost:8000/movements/{movement_id}",
                    headers={"Authorization": f"Bearer {self.token}"}
                )
                
                if response.status_code == 200:
                    QMessageBox.information(self, "Éxito", "Movimiento eliminado correctamente")
                    self.load_movements()
                else:
                    QMessageBox.warning(self, "Error", "No se pudo eliminar el movimiento")
            
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al eliminar movimiento: {str(e)}")

    def show_add_corredor_dialog(self):
        """Muestra el diálogo para agregar un nuevo corredor"""
        dialog = CorredorDialog(self.token, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_corredores()

    def show_edit_corredor_dialog(self, corredor_id):
        """Muestra el diálogo para editar un corredor existente"""
        dialog = CorredorDialog(self.token, corredor_id=corredor_id, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
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
                    f"http://localhost:8000/corredores/{corredor_id}",
                    headers={"Authorization": f"Bearer {self.token}"}
                )
                
                if response.status_code == 200:
                    QMessageBox.information(self, "Éxito", "Corredor eliminado correctamente")
                    self.load_corredores()
                else:
                    QMessageBox.warning(self, "Error", "No se pudo eliminar el corredor")
            
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al eliminar corredor: {str(e)}")

class ClientDialog(QDialog):
    def __init__(self, token, client_id=None, parent=None):
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
        layout = QFormLayout(self)
        
        # Campos del formulario
        self.nombres_input = QLineEdit()
        self.apellidos_input = QLineEdit()
        self.tipo_documento_input = QComboBox()
        self.tipo_documento_input.addItems(["DNI", "CI", "RUT", "CUIT"])
        self.documentos_input = QLineEdit()
        self.fecha_nacimiento_input = QDateEdit()
        self.fecha_nacimiento_input.setCalendarPopup(True)
        self.direccion_input = QLineEdit()
        self.localidad_input = QLineEdit()
        self.telefonos_input = QLineEdit()
        self.movil_input = QLineEdit()
        self.mail_input = QLineEdit()
        self.observaciones_input = QTextEdit()
        
        # Agregar campos al layout
        layout.addRow("Nombres:", self.nombres_input)
        layout.addRow("Apellidos:", self.apellidos_input)
        layout.addRow("Tipo de Documento:", self.tipo_documento_input)
        layout.addRow("Número de Documento:", self.documentos_input)
        layout.addRow("Fecha de Nacimiento:", self.fecha_nacimiento_input)
        layout.addRow("Dirección:", self.direccion_input)
        layout.addRow("Localidad:", self.localidad_input)
        layout.addRow("Teléfonos:", self.telefonos_input)
        layout.addRow("Móvil:", self.movil_input)
        layout.addRow("Mail:", self.mail_input)
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
    
    def load_client_data(self):
        """Carga los datos del cliente para edición"""
        try:
            response = requests.get(
                f"http://localhost:8000/clients/{self.client_id}",
                headers={"Authorization": f"Bearer {self.token}"}
            )
            
            if response.status_code == 200:
                client = response.json()
                self.nombres_input.setText(client["nombres"])
                self.apellidos_input.setText(client["apellidos"])
                self.tipo_documento_input.setCurrentText(client["tipo_documento"])
                self.documentos_input.setText(client["documento"])
                self.fecha_nacimiento_input.setDate(QDate.fromString(client["fecha_nacimiento"], Qt.DateFormat.ISODate))
                self.direccion_input.setText(client["direccion"])
                self.localidad_input.setText(client["localidad"] or "")
                self.telefonos_input.setText(client["telefonos"])
                self.movil_input.setText(client["movil"])
                self.mail_input.setText(client["mail"])
                self.observaciones_input.setPlainText(client["observaciones"] or "")
            else:
                QMessageBox.warning(self, "Error", "No se pudo cargar los datos del cliente")
                self.reject()
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar datos del cliente: {str(e)}")
            self.reject()
    
    def save_client(self):
        """Guarda los datos del cliente"""
        try:
            # Validar campos requeridos
            if not all([
                self.apellidos_input.text().strip(),  # Solo apellidos es requerido
                self.direccion_input.text().strip()   # Solo dirección es requerida
            ]):
                QMessageBox.warning(self, "Error", "Por favor complete al menos los campos Apellidos y Dirección")
                return

            data = {
                "nombres": self.nombres_input.text().strip(),
                "apellidos": self.apellidos_input.text().strip(),
                "tipo_documento": self.tipo_documento_input.currentText() if self.tipo_documento_input.currentText() != "" else None,
                "documento": self.documentos_input.text().strip(),
                "fecha_nacimiento": self.fecha_nacimiento_input.date().toString(Qt.DateFormat.ISODate) if not self.fecha_nacimiento_input.date().isNull() else None,
                "direccion": self.direccion_input.text().strip(),
                "localidad": self.localidad_input.text().strip() or None,
                "telefonos": self.telefonos_input.text().strip(),
                "movil": self.movil_input.text().strip(),
                "mail": self.mail_input.text().strip(),
                "observaciones": self.observaciones_input.toPlainText().strip() or None
            }
            
            if self.client_id:
                # Actualizar cliente existente
                response = requests.put(
                    f"http://localhost:8000/clients/{self.client_id}",
                    json=data,
                    headers={"Authorization": f"Bearer {self.token}"}
                )
            else:
                # Crear nuevo cliente
                response = requests.post(
                    "http://localhost:8000/clients",
                    json=data,
                    headers={"Authorization": f"Bearer {self.token}"}
                )
            
            if response.status_code in [200, 201]:
                QMessageBox.information(
                    self,
                    "Éxito",
                    "Cliente guardado correctamente"
                )
                self.accept()
            else:
                error_msg = "Error al guardar el cliente"
                try:
                    error_data = response.json()
                    if "detail" in error_data:
                        if isinstance(error_data["detail"], list):
                            error_msg = "\n".join([err["msg"] for err in error_data["detail"]])
                        else:
                            error_msg = error_data["detail"]
                except:
                    if response.text:
                        error_msg = f"{error_msg}: {response.text}"
                QMessageBox.warning(self, "Error", error_msg)
        
        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", f"Error de conexión: {str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error inesperado: {str(e)}")

class MovementDialog(QDialog):
    def __init__(self, token, movement_id=None, parent=None):
        super().__init__(parent)
        self.token = token
        self.movement_id = movement_id
        self.setup_ui()
        
        if movement_id:
            self.setWindowTitle("Editar Movimiento")
            self.load_movement_data()
        else:
            self.setWindowTitle("Agregar Movimiento")
    
    def setup_ui(self):
        """Configura la interfaz del diálogo"""
        layout = QFormLayout(self)
        
        # Campos del formulario
        self.Cliente_input = QLineEdit()  # Campo para mostrar/editar el ID
        self.Cliente_input.setReadOnly(True)  # Solo lectura
        self.cliente_selector = QComboBox()  # Selector de cliente
        self.load_clients()  # Cargar la lista de clientes
        
        # Cuando se selecciona un cliente, actualizar el campo Cliente_input
        self.cliente_selector.currentIndexChanged.connect(self.update_cliente_id)
        
        # Layout para cliente (ID y selector)
        cliente_layout = QHBoxLayout()
        cliente_layout.addWidget(self.Cliente_input)
        cliente_layout.addWidget(self.cliente_selector)
        
        self.FechaMov_input = QDateEdit()
        self.FechaMov_input.setCalendarPopup(True)
        self.FechaMov_input.setDate(QDate.currentDate())
        self.Corredor_input = QLineEdit()
        self.Tipo_seguro_input = QLineEdit()
        self.Carpeta_input = QLineEdit()
        self.Poliza_input = QLineEdit()
        self.Endoso_input = QLineEdit()
        self.Vto_Desde_input = QDateEdit()
        self.Vto_Desde_input.setCalendarPopup(True)
        self.Vto_Desde_input.setDate(QDate.currentDate())
        self.Vto_Hasta_input = QDateEdit()
        self.Vto_Hasta_input.setCalendarPopup(True)
        self.Vto_Hasta_input.setDate(QDate.currentDate())
        self.Moneda_input = QComboBox()
        self.Moneda_input.addItems(["$", "U$S"])
        self.Premio_input = QLineEdit()
        self.Cuotas_input = QLineEdit()
        self.Observaciones_input = QTextEdit()
        
        # Agregar campos al layout
        layout.addRow("Cliente:", cliente_layout)
        layout.addRow("Fecha de Movimiento:", self.FechaMov_input)
        layout.addRow("Corredor:", self.Corredor_input)
        layout.addRow("Tipo de Seguro:", self.Tipo_seguro_input)
        layout.addRow("Carpeta:", self.Carpeta_input)
        layout.addRow("Póliza:", self.Poliza_input)
        layout.addRow("Endoso:", self.Endoso_input)
        layout.addRow("Vigencia Desde:", self.Vto_Desde_input)
        layout.addRow("Vigencia Hasta:", self.Vto_Hasta_input)
        layout.addRow("Moneda:", self.Moneda_input)
        layout.addRow("Premio:", self.Premio_input)
        layout.addRow("Cuotas:", self.Cuotas_input)
        layout.addRow("Observaciones:", self.Observaciones_input)
        
        # Botones
        button_box = QHBoxLayout()
        save_button = QPushButton("Guardar")
        save_button.clicked.connect(self.save_movement)
        cancel_button = QPushButton("Cancelar")
        cancel_button.clicked.connect(self.reject)
        
        button_box.addWidget(save_button)
        button_box.addWidget(cancel_button)
        layout.addRow(button_box)
    
    def load_clients(self):
        """Carga la lista de clientes en el combo box"""
        try:
            response = requests.get(
                "http://localhost:8000/clients",
                headers={"Authorization": f"Bearer {self.token}"}
            )
            
            if response.status_code == 200:
                clients = response.json()
                for client in clients:
                    # Mostrar ID y nombre, guardar el ID
                    self.cliente_selector.addItem(
                        f"{client['id']} - {client['nombres']} {client['apellidos']}",
                        userData=client['id']
                    )
            else:
                QMessageBox.warning(self, "Error", "No se pudieron cargar los clientes")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar clientes: {str(e)}")

    def update_cliente_id(self):
        """Actualiza el campo de ID cuando se selecciona un cliente"""
        selected_id = self.cliente_selector.currentData()
        if selected_id is not None:
            self.Cliente_input.setText(str(selected_id))

    def load_movement_data(self):
        """Carga los datos del movimiento para edición"""
        try:
            response = requests.get(
                f"http://localhost:8000/movements/{self.movement_id}",
                headers={"Authorization": f"Bearer {self.token}"}
            )
            
            if response.status_code == 200:
                movement = response.json()
                # Buscar y seleccionar el cliente correcto en el combo box
                index = self.cliente_selector.findData(movement["Cliente"])
                if index >= 0:
                    self.cliente_selector.setCurrentIndex(index)
                self.Cliente_input.setText(str(movement["Cliente"]))
                self.FechaMov_input.setDate(QDate.fromString(movement["FechaMov"], Qt.DateFormat.ISODate))
                self.Corredor_input.setText(str(movement["Corredor"]))
                self.Tipo_seguro_input.setText(str(movement["Tipo_seguro"]))
                self.Carpeta_input.setText(movement["Carpeta"])
                self.Poliza_input.setText(movement["Poliza"] or "")
                self.Endoso_input.setText(movement["Endoso"] or "")
                self.Vto_Desde_input.setDate(QDate.fromString(movement["Vto_Desde"], Qt.DateFormat.ISODate))
                self.Vto_Hasta_input.setDate(QDate.fromString(movement["Vto_Hasta"], Qt.DateFormat.ISODate))
                self.Moneda_input.setCurrentText(movement["Moneda"])
                self.Premio_input.setText(str(movement["Premio"] or ""))
                self.Cuotas_input.setText(str(movement["Cuotas"] or ""))
                self.Observaciones_input.setPlainText(movement["Observaciones"] or "")
            else:
                QMessageBox.warning(self, "Error", "No se pudo cargar los datos del movimiento")
                self.reject()
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar datos del movimiento: {str(e)}")
            self.reject()
    
    def save_movement(self):
        """Guarda los datos del movimiento"""
        try:
            # Validar campos requeridos
            if not all([
                self.Cliente_input.text().strip(),  # Usar el ID del cliente
                self.Corredor_input.text().strip(),
                self.Tipo_seguro_input.text().strip(),
                self.Carpeta_input.text().strip()
            ]):
                QMessageBox.warning(self, "Error", "Por favor complete los campos obligatorios")
                return

            # Convertir premio y cuotas a números si no están vacíos
            premio = None
            if self.Premio_input.text().strip():
                try:
                    premio = float(self.Premio_input.text().strip())
                except ValueError:
                    QMessageBox.warning(self, "Error", "El premio debe ser un número válido")
                    return

            cuotas = None
            if self.Cuotas_input.text().strip():
                try:
                    cuotas = int(self.Cuotas_input.text().strip())
                except ValueError:
                    QMessageBox.warning(self, "Error", "El número de cuotas debe ser un número entero")
                    return

            data = {
                "Cliente": int(self.Cliente_input.text().strip()),  # Convertir a entero
                "FechaMov": self.FechaMov_input.date().toString(Qt.DateFormat.ISODate),
                "Corredor": int(self.Corredor_input.text().strip()),
                "Tipo_seguro": int(self.Tipo_seguro_input.text().strip()),
                "Carpeta": self.Carpeta_input.text().strip(),
                "Poliza": self.Poliza_input.text().strip() or None,
                "Endoso": self.Endoso_input.text().strip() or None,
                "Vto_Desde": self.Vto_Desde_input.date().toString(Qt.DateFormat.ISODate),
                "Vto_Hasta": self.Vto_Hasta_input.date().toString(Qt.DateFormat.ISODate),
                "Moneda": self.Moneda_input.currentText(),
                "Premio": premio,
                "Cuotas": cuotas,
                "Observaciones": self.Observaciones_input.toPlainText().strip() or None
            }
            
            if self.movement_id:
                # Actualizar movimiento existente
                response = requests.put(
                    f"http://localhost:8000/movements/{self.movement_id}",
                    json=data,
                    headers={"Authorization": f"Bearer {self.token}"}
                )
            else:
                # Crear nuevo movimiento
                response = requests.post(
                    "http://localhost:8000/movements",
                    json=data,
                    headers={"Authorization": f"Bearer {self.token}"}
                )
            
            if response.status_code in [200, 201]:
                QMessageBox.information(
                    self,
                    "Éxito",
                    "Movimiento guardado correctamente"
                )
                self.accept()
            else:
                error_msg = "Error al guardar el movimiento"
                try:
                    error_data = response.json()
                    if "detail" in error_data:
                        if isinstance(error_data["detail"], list):
                            error_msg = "\n".join([err["msg"] for err in error_data["detail"]])
                        else:
                            error_msg = error_data["detail"]
                except:
                    if response.text:
                        error_msg = f"{error_msg}: {response.text}"
                QMessageBox.warning(self, "Error", error_msg)
        
        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", f"Error de conexión: {str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error inesperado: {str(e)}")

class CorredorDialog(QDialog):
    def __init__(self, token, corredor_id=None, parent=None):
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
        layout = QVBoxLayout()
        
        # Formulario de corredor
        from .ui.views.corredor_form import CorredorForm
        self.form = CorredorForm()
        layout.addWidget(self.form)
        
        # Botones
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Guardar")
        self.cancel_button = QPushButton("Cancelar")
        
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
        # Conexiones
        self.save_button.clicked.connect(self.save_corredor)
        self.cancel_button.clicked.connect(self.reject)

    def load_corredor_data(self):
        """Carga los datos del corredor para edición"""
        try:
            response = requests.get(
                f"http://localhost:8000/corredores/{self.corredor_id}",
                headers={"Authorization": f"Bearer {self.token}"}
            )
            response.raise_for_status()
            corredor_data = response.json()
            self.form.set_data(corredor_data)
        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", f"Error al cargar datos del corredor: {str(e)}")

    def save_corredor(self):
        """Guarda los datos del corredor"""
        try:
            data = self.form.get_data()
            
            if self.corredor_id:  # Actualizar corredor existente
                response = requests.put(
                    f"http://localhost:8000/corredores/{self.corredor_id}",
                    json=data,
                    headers={"Authorization": f"Bearer {self.token}"}
                )
            else:  # Crear nuevo corredor
                response = requests.post(
                    "http://localhost:8000/corredores/",
                    json=data,
                    headers={"Authorization": f"Bearer {self.token}"}
                )
            
            response.raise_for_status()
            QMessageBox.information(self, "Éxito", "Corredor guardado exitosamente")
            self.accept()
        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", f"Error al guardar corredor: {str(e)}")
