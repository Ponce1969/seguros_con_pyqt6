from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from .database import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)  # UUID como clave primaria
    nombres = Column(String(30), nullable=False)  # Nombre del cliente
    apellidos = Column(String(30), nullable=False)  # Apellido del cliente
    tipo_documento = Column(String(4), nullable=False)  # Tipo de documento (DNI, CI, RUT, CUIT)
    documento = Column(String(20), nullable=False, unique=True, index=True)  # Número de documento
    fecha_nacimiento = Column(Date, nullable=False)  # Fecha de nacimiento
    direccion = Column(String(70), nullable=False)  # Dirección
    localidad = Column(String(15))  # Localidad
    telefonos = Column(String(20), nullable=False)  # Teléfonos
    movil = Column(String(20), nullable=False)  # Móvil
    email = Column(String(50), nullable=False, unique=True, index=True)  # Correo electrónico
    corredor = Column(Integer)  # ID del corredor (si aplica)
    observaciones = Column(Text)  # Observaciones adicionales
    creado_por_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    modificado_por_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_modificacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relación con el usuario que creó el registro
    creado_por_usuario = relationship("User", foreign_keys=[creado_por_id], back_populates="clientes_creados")
    modificado_por_usuario = relationship("User", foreign_keys=[modificado_por_id], back_populates="clientes_modificados")

    # Relación uno a muchos con MovimientoVigencia
    movimientos_vigencias = relationship("MovimientoVigencia", back_populates="cliente_rel", cascade="all, delete-orphan")

class Corredor(Base):
    __tablename__ = "corredores"

    numero = Column(Integer, primary_key=True)  # Número de corredor
    nombres = Column(String(30))  # Puede ser vacío para empresas
    apellidos = Column(String(30), nullable=False)  # Apellidos o nombre de empresa
    documento = Column(String(20), nullable=False, unique=True)
    direccion = Column(String(70), nullable=False)
    localidad = Column(String(15), nullable=False)
    telefonos = Column(String(15))  # Puede ser vacío
    movil = Column(String(15))  # Puede ser vacío
    mail = Column(String(40), nullable=False)
    observaciones = Column(Text)

    # Relación uno a muchos con MovimientoVigencia
    movimientos = relationship("MovimientoVigencia", back_populates="corredor_rel")

class TipoSeguro(Base):
    __tablename__ = "tipos_de_seguros"

    id_tipo = Column(Integer, primary_key=True)  # ID único del tipo de seguro
    aseguradora = Column(String(15), nullable=False)  # Nombre de la compañía aseguradora
    codigo = Column(String(5), nullable=False)  # Código de la cartera
    descripcion = Column(String(30), nullable=False)  # Descripción del tipo de seguro

    # Relación uno a muchos con MovimientoVigencia
    movimientos = relationship("MovimientoVigencia", back_populates="tipo_seguro_rel")

class MovimientoVigencia(Base):
    __tablename__ = "movimientos_vigencias"

    id_movimiento = Column(Integer, primary_key=True, autoincrement=True, index=True)
    fecha_mov = Column(Date, nullable=False)
    corredor = Column(Integer, ForeignKey("corredores.numero"), nullable=False)
    # Referencia al UUID del cliente en nuestra base de datos
    cliente_id = Column(UUID(as_uuid=True), ForeignKey("clientes.id"), nullable=False)
    # Número de cliente asignado por la compañía de seguros
    numero_cliente_compania = Column(String, nullable=True)
    tipo_seguro = Column(Integer, ForeignKey("tipos_de_seguros.id_tipo"), nullable=False)
    carpeta = Column(String, nullable=False)
    poliza = Column(String)
    endoso = Column(String)
    vto_desde = Column(Date, nullable=False)
    vto_hasta = Column(Date, nullable=False)
    moneda = Column(String, nullable=False)  # '$' o 'U$S'
    premio = Column(Float)
    cuotas = Column(Integer)
    observaciones = Column(Text)

    # Relación con el cliente (uno a muchos)
    cliente_rel = relationship("Cliente", back_populates="movimientos_vigencias")
    corredor_rel = relationship("Corredor", back_populates="movimientos")
    tipo_seguro_rel = relationship("TipoSeguro", back_populates="movimientos")

class SystemConfig(Base):
    __tablename__ = "system_config"

    id = Column(Integer, primary_key=True)
    first_run_completed = Column(Boolean, default=False)
    setup_date = Column(DateTime, default=datetime.utcnow)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    email = Column(String(64), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    is_active = Column(Boolean, default=True)  # Reemplaza User_Validado por un booleano más estándar
    role = Column(String(20), default="user")  # Para diferentes niveles de acceso
    comision_porcentaje = Column(Float, default=0.0)  # Porcentaje de comisión del usuario
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    ultima_modificacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    clientes_creados = relationship("Cliente", back_populates="creado_por_usuario", 
                                  foreign_keys="Cliente.creado_por_id")
    clientes_modificados = relationship("Cliente", back_populates="modificado_por_usuario",
                                      foreign_keys="Cliente.modificado_por_id")