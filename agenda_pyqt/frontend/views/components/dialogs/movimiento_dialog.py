from PyQt6.QtWidgets import (QDialog, QFormLayout, QLineEdit, QTextEdit,
                            QPushButton, QHBoxLayout, QMessageBox, QComboBox,
                            QDateEdit, QDoubleSpinBox, QSpinBox)
from PyQt6.QtCore import QDate, QTimer
import requests
from datetime import datetime
import logging
import traceback

logger = logging.getLogger(__name__)

class MovimientoDialog(QDialog):
    def __init__(self, parent=None, movement_id=None, token=None):
        super().__init__(parent)
        self.token = token
        self.movement_id = movement_id
        self.setup_ui()
        
        if movement_id:
            self.setWindowTitle("Editar Movimiento")
            self.load_movement_data()
        else:
            self.setWindowTitle("Agregar Movimiento")
            # Establecer fecha actual por defecto
            self.fecha_mov_input.setDate(QDate.currentDate())
            self.vto_desde_input.setDate(QDate.currentDate())
            self.vto_hasta_input.setDate(QDate.currentDate().addYears(1))

    def setup_ui(self):
        """Configura la interfaz del diálogo"""
        self.setMinimumWidth(600)  # Aumentado de 400 a 600
        self.setMinimumHeight(500)  # Agregado altura mínima
        layout = QFormLayout(self)
        layout.setSpacing(10)

        # Campos de entrada
        self.fecha_mov_input = QDateEdit()
        self.fecha_mov_input.setCalendarPopup(True)
        self.fecha_mov_input.setDate(QDate.currentDate())
        self.fecha_mov_input.setMinimumWidth(200)  # Ancho mínimo para la fecha

        self.corredor_input = QComboBox()
        self.corredor_input.currentIndexChanged.connect(self.on_corredor_changed)
        self.corredor_input.setMinimumWidth(300)  # Ancho mínimo para el corredor
        
        # Agregar campo de búsqueda de clientes
        self.cliente_search = QLineEdit()
        self.cliente_search.setPlaceholderText("Buscar cliente por nombre, documento o email...")
        self.cliente_search.setMinimumWidth(300)
        self.cliente_search.textChanged.connect(self.on_cliente_search_changed)
        self.cliente_search_timer = QTimer()
        self.cliente_search_timer.setSingleShot(True)
        self.cliente_search_timer.timeout.connect(self.search_clientes)
        
        self.cliente_input = QComboBox()
        self.cliente_input.setMinimumWidth(300)
        
        # Botón para ver todos los clientes
        self.ver_todos_button = QPushButton("Ver todos")
        self.ver_todos_button.clicked.connect(self.load_all_clientes)
        
        # Layout horizontal para búsqueda y botón
        search_layout = QHBoxLayout()
        search_layout.addWidget(self.cliente_search)
        search_layout.addWidget(self.ver_todos_button)

        # Tipo de seguro como SpinBox
        self.tipo_seguro_input = QSpinBox()
        self.tipo_seguro_input.setMinimum(100)
        self.tipo_seguro_input.setMaximum(999)
        self.tipo_seguro_input.setToolTip("100: Seguros Generales, 120: Hogar, 130: Vehículos")
        
        self.carpeta_input = QLineEdit()
        self.poliza_input = QLineEdit()
        self.endoso_input = QLineEdit()
        
        self.vto_desde_input = QDateEdit()
        self.vto_desde_input.setCalendarPopup(True)
        self.vto_desde_input.setDate(QDate.currentDate())
        
        self.vto_hasta_input = QDateEdit()
        self.vto_hasta_input.setCalendarPopup(True)
        self.vto_hasta_input.setDate(QDate.currentDate().addYears(1))
        
        # Campos numéricos
        self.moneda_input = QComboBox()
        self.moneda_input.addItems(["$", "U$S"])
        
        self.premio_input = QDoubleSpinBox()
        self.premio_input.setMaximum(999999999.99)
        self.premio_input.setDecimals(2)
        
        self.cuotas_input = QSpinBox()
        self.cuotas_input.setMaximum(36)
        self.cuotas_input.setMinimum(1)
        
        self.observaciones_input = QTextEdit()
        self.observaciones_input.setMaximumHeight(100)

        # Cargar datos para los combos
        self.load_corredores()

        # Agregar campos al layout
        layout.addRow("Fecha Movimiento *:", self.fecha_mov_input)
        layout.addRow("Corredor *:", self.corredor_input)
        layout.addRow("Buscar Cliente:", search_layout)
        layout.addRow("Cliente *:", self.cliente_input)
        layout.addRow("Tipo de Seguro *:", self.tipo_seguro_input)
        layout.addRow("Carpeta:", self.carpeta_input)
        layout.addRow("Póliza *:", self.poliza_input)
        layout.addRow("Endoso:", self.endoso_input)
        layout.addRow("Vigencia Desde *:", self.vto_desde_input)
        layout.addRow("Vigencia Hasta *:", self.vto_hasta_input)
        layout.addRow("Moneda *:", self.moneda_input)
        layout.addRow("Premio *:", self.premio_input)
        layout.addRow("Cuotas *:", self.cuotas_input)
        layout.addRow("Observaciones:", self.observaciones_input)

        # Botones
        button_box = QHBoxLayout()
        save_button = QPushButton("Guardar")
        save_button.clicked.connect(self.save_movement)
        cancel_button = QPushButton("Cancelar")
        cancel_button.clicked.connect(self.reject)
        
        button_box.addWidget(save_button)
        button_box.addWidget(cancel_button)
        layout.addRow(button_box)

    def on_corredor_changed(self, index):
        """Maneja el cambio de selección en el combobox de corredor"""
        # Limpiar el combo de clientes y el campo de búsqueda
        self.cliente_input.clear()
        self.cliente_search.clear()
        
        if index <= 0:  # No hay corredor seleccionado
            return
            
        corredor_numero = self.corredor_input.itemData(index)
        if not corredor_numero:
            return
            
        try:
            # Cargar los primeros 10 clientes del corredor
            self.load_clientes_por_corredor(corredor_numero)
        except Exception as e:
            logger.error(f"Error al cargar clientes iniciales: {str(e)}")
            QMessageBox.critical(self, "Error", f"Error al cargar clientes: {str(e)}")

    def on_cliente_search_changed(self, text):
        """Maneja el cambio en el campo de búsqueda"""
        # Reiniciar el timer cada vez que el texto cambia
        self.cliente_search_timer.stop()
        # Iniciar el timer con 300ms de retraso
        self.cliente_search_timer.start(300)

    def search_clientes(self):
        """Realiza la búsqueda de clientes"""
        search_text = self.cliente_search.text().strip()
        corredor_index = self.corredor_input.currentIndex()
        
        if corredor_index == -1:
            QMessageBox.warning(self, "Error", "Por favor seleccione un corredor primero")
            return
            
        corredor_numero = self.corredor_input.itemData(corredor_index)
        if not corredor_numero:
            logger.error("No se pudo obtener el número de corredor")
            return
            
        try:
            self.load_clientes_por_corredor(corredor_numero, search=search_text)
        except Exception as e:
            logger.error(f"Error al buscar clientes: {str(e)}")
            QMessageBox.critical(self, "Error", f"Error al buscar clientes: {str(e)}")

    def load_all_clientes(self):
        """Carga todos los clientes del corredor seleccionado"""
        corredor_index = self.corredor_input.currentIndex()
        
        if corredor_index == -1:
            QMessageBox.warning(self, "Error", "Por favor seleccione un corredor primero")
            return
            
        corredor_numero = self.corredor_input.itemData(corredor_index)
        if not corredor_numero:
            logger.error("No se pudo obtener el número de corredor")
            return
            
        try:
            # Cargar todos los clientes (sin límite)
            self.load_clientes_por_corredor(corredor_numero, limit=None)
        except Exception as e:
            logger.error(f"Error al cargar todos los clientes: {str(e)}")
            QMessageBox.critical(self, "Error", f"Error al cargar todos los clientes: {str(e)}")

    def load_clientes_por_corredor(self, corredor_numero, search=None, limit=10):
        """Carga la lista de clientes para un corredor específico"""
        try:
            logger.debug(f"Realizando petición GET para corredor {corredor_numero}")
            logger.debug(f"Parámetros: search={search}, limit={limit}")
            
            params = {}
            if limit:
                params["limit"] = limit
            if search:
                params["search"] = search
            
            url = f"http://localhost:8000/api/v1/clientes/por-corredor/{corredor_numero}"
            logger.debug(f"URL: {url}")
            
            response = requests.get(
                url,
                headers={"Authorization": f"Bearer {self.token}"},
                params=params
            )
            logger.debug(f"Código de respuesta: {response.status_code}")
            
            if response.status_code != 200:
                logger.error(f"Error en la respuesta: {response.text}")
                raise requests.RequestException(f"Status code: {response.status_code}, Response: {response.text}")
                
            response.raise_for_status()
            clientes = response.json()
            
            # Debug para ver la estructura de la respuesta
            logger.debug(f"Estructura de la respuesta: {clientes}")
            
            # Limpiar el combo actual
            self.cliente_input.clear()
            
            # Agregar los clientes al combo
            for cliente in clientes:
                try:
                    # Obtener los campos de manera segura usando .get()
                    apellidos = cliente.get('apellidos', '')
                    nombres = cliente.get('nombres', '')
                    tipo_documento = cliente.get('tipo_documento', '')
                    nro_documento = cliente.get('nro_documento', '')  # Cambiado de 'documento' a 'nro_documento'
                    mail = cliente.get('mail', '')
                    
                    # Crear un texto descriptivo con la información del cliente
                    display_text = f"[{cliente.get('numero_cliente', '')}] {apellidos}, {nombres}"
                    if nro_documento:
                        display_text += f" - {tipo_documento}: {nro_documento}"
                    if mail:
                        display_text += f" ({mail})"
                        
                    self.cliente_input.addItem(display_text, cliente.get('numero_cliente'))
                    
                except Exception as e:
                    logger.error(f"Error al procesar cliente: {cliente}")
                    logger.error(f"Error: {str(e)}")
                    continue
                
            if self.cliente_input.count() == 0:
                self.cliente_input.addItem("No se encontraron clientes", None)
                
        except Exception as e:
            logger.error(f"Error al cargar clientes: {str(e)}")
            raise

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
                display_text = f"{corredor['apellidos']}, {corredor.get('nombres', '')} ({corredor['numero']})"
                self.corredor_input.addItem(display_text, corredor['numero'])
                
        except requests.RequestException as e:
            logger.error(f"Error al cargar corredores: {str(e)}")
            QMessageBox.critical(self, "Error", f"Error al cargar corredores: {str(e)}")

    def load_movement_data(self):
        """Carga los datos del movimiento para edición"""
        try:
            response = requests.get(
                f"http://localhost:8000/api/v1/movimientos/{self.movement_id}",
                headers={"Authorization": f"Bearer {self.token}"}
            )
            response.raise_for_status()
            movimiento = response.json()

            # Seleccionar cliente usando numero_cliente
            index = self.cliente_input.findData(movimiento["Cliente"])
            if index >= 0:
                self.cliente_input.setCurrentIndex(index)
            else:
                # Si no se encuentra el cliente, cargar sus datos
                try:
                    cliente_response = requests.get(
                        f"http://localhost:8000/api/v1/clientes/{movimiento['Cliente']}",
                        headers={"Authorization": f"Bearer {self.token}"}
                    )
                    cliente_response.raise_for_status()
                    cliente = cliente_response.json()
                    display_text = f"[{cliente.get('numero_cliente', '')}] {cliente.get('apellidos', '')}, {cliente.get('nombres', '')}"
                    self.cliente_input.addItem(display_text, cliente.get('numero_cliente'))
                    self.cliente_input.setCurrentIndex(self.cliente_input.count() - 1)
                except:
                    logger.error(f"No se pudo cargar el cliente {movimiento['Cliente']}")

            # Seleccionar corredor
            index = self.corredor_input.findData(movimiento["Corredor"])
            if index >= 0:
                self.corredor_input.setCurrentIndex(index)

            self.fecha_mov_input.setDate(QDate.fromString(movimiento["FechaMov"], "yyyy-MM-dd"))
            self.tipo_seguro_input.setValue(movimiento["Tipo_seguro"])
            self.carpeta_input.setText(movimiento.get("Carpeta", ""))
            self.poliza_input.setText(movimiento["Poliza"])
            self.endoso_input.setText(movimiento.get("Endoso", ""))
            self.vto_desde_input.setDate(QDate.fromString(movimiento["Vto_Desde"], "yyyy-MM-dd"))
            self.vto_hasta_input.setDate(QDate.fromString(movimiento["Vto_Hasta"], "yyyy-MM-dd"))
            index = self.moneda_input.findText(movimiento.get("Moneda", "$"))
            if index >= 0:
                self.moneda_input.setCurrentIndex(index)
            self.premio_input.setValue(movimiento["Premio"])
            self.cuotas_input.setValue(movimiento["Cuotas"])
            self.observaciones_input.setText(movimiento.get("Observaciones", ""))

        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", f"Error al cargar datos del movimiento: {str(e)}")
            self.reject()

    def save_movement(self):
        """Guarda los datos del movimiento"""
        # Validar cliente seleccionado
        numero_cliente = self.cliente_input.currentData()
        if not numero_cliente:
            QMessageBox.warning(self, "Error", "Debe seleccionar un cliente")
            return

        # Validar corredor seleccionado
        corredor_id = self.corredor_input.currentData()
        if not corredor_id:
            QMessageBox.warning(self, "Error", "Debe seleccionar un corredor")
            return

        data = {
            "FechaMov": self.fecha_mov_input.date().toString("yyyy-MM-dd"),
            "Corredor": corredor_id,
            "Cliente": numero_cliente,
            "Tipo_seguro": self.tipo_seguro_input.value(),
            "Carpeta": self.carpeta_input.text().strip(),
            "Poliza": self.poliza_input.text().strip(),
            "Endoso": self.endoso_input.text().strip(),
            "Vto_Desde": self.vto_desde_input.date().toString("yyyy-MM-dd"),
            "Vto_Hasta": self.vto_hasta_input.date().toString("yyyy-MM-dd"),
            "Moneda": self.moneda_input.currentText(),
            "Premio": self.premio_input.value(),
            "Cuotas": self.cuotas_input.value(),
            "Observaciones": self.observaciones_input.toPlainText().strip()
        }

        # Log de los datos que se enviarán
        logger.debug(f"Datos a enviar al backend: {data}")

        # Validaciones básicas
        campos_requeridos = [
            "FechaMov", "Corredor", "Cliente", "Tipo_seguro",
            "Poliza", "Vto_Desde", "Vto_Hasta", "Premio", "Cuotas"
        ]
        campos_vacios = [campo for campo in campos_requeridos if not data[campo]]
        
        if campos_vacios:
            campos = ", ".join(campos_vacios)
            QMessageBox.warning(self, "Error", f"Los siguientes campos son obligatorios: {campos}")
            return

        try:
            if self.movement_id:  # Editar movimiento existente
                response = requests.put(
                    f"http://localhost:8000/api/v1/movimientos/{self.movement_id}",
                    headers={"Authorization": f"Bearer {self.token}"},
                    json=data
                )
            else:  # Crear nuevo movimiento
                logger.debug("Enviando solicitud POST para crear nuevo movimiento")
                response = requests.post(
                    "http://localhost:8000/api/v1/movimientos/",
                    headers={"Authorization": f"Bearer {self.token}"},
                    json=data
                )
            
            if response.status_code >= 400:
                logger.error(f"Error del servidor: {response.status_code}")
                logger.error(f"Respuesta del servidor: {response.text}")
                
            response.raise_for_status()
            QMessageBox.information(self, "Éxito", "Movimiento guardado exitosamente")
            self.accept()

        except requests.RequestException as e:
            error_msg = f"Error al guardar movimiento: {str(e)}"
            if hasattr(e.response, 'text'):
                error_msg += f"\nDetalles: {e.response.text}"
            logger.error(error_msg)
            QMessageBox.critical(self, "Error", error_msg)
