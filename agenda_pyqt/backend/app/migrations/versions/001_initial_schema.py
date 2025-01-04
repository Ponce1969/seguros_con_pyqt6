"""Initial database schema with secure client numbering."""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '001_initial_schema'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Crear tabla usuarios
    op.create_table(
        'usuarios',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('is_superuser', sa.Boolean(), default=False),
        sa.Column('fecha_creacion', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('fecha_modificacion', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_usuario_email', 'usuarios', ['email'], unique=True)
    op.create_index('idx_usuario_username', 'usuarios', ['username'], unique=True)

    # Crear secuencia para números de cliente
    op.execute("CREATE SEQUENCE IF NOT EXISTS cliente_numero_seq START 1000")
    
    # Crear tabla clientes
    op.create_table(
        'clientes',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('numero_cliente', sa.BigInteger(), nullable=False),
        sa.Column('nombres', sa.String(100), nullable=True),
        sa.Column('apellidos', sa.String(100), nullable=False),
        sa.Column('tipo_documento', sa.String(50), nullable=True),
        sa.Column('documentos', sa.String(50), nullable=True),
        sa.Column('fecha_nacimiento', sa.Date(), nullable=True),
        sa.Column('direccion', sa.String(200), nullable=False),
        sa.Column('localidad', sa.String(50), nullable=True),
        sa.Column('telefonos', sa.String(100), nullable=True),
        sa.Column('movil', sa.String(100), nullable=True),
        sa.Column('mail', sa.String(100), nullable=True),
        sa.Column('corredor', sa.Integer(), nullable=True),
        sa.Column('observaciones', sa.Text(), nullable=True),
        sa.Column('creado_por_id', sa.Integer(), nullable=False),
        sa.Column('modificado_por_id', sa.Integer(), nullable=False),
        sa.Column('fecha_creacion', sa.DateTime(), nullable=False),
        sa.Column('fecha_modificacion', sa.DateTime(), nullable=False)
    )
    
    # Crear índices para clientes
    op.create_index('idx_cliente_numero', 'clientes', ['numero_cliente'], unique=True)
    op.create_index('idx_cliente_documento', 'clientes', ['documentos'], unique=True)
    op.create_index('idx_cliente_mail', 'clientes', ['mail'], unique=True)
    op.create_index('idx_cliente_corredor', 'clientes', ['corredor'])
    
    # Crear tabla movimientos_vigencias
    op.create_table(
        'movimientos_vigencias',
        sa.Column('Id_movimiento', sa.Integer(), primary_key=True),
        sa.Column('FechaMov', sa.Date(), nullable=False),
        sa.Column('Corredor', sa.Integer(), nullable=False),
        sa.Column('Cliente', sa.BigInteger(), nullable=False),
        sa.Column('Tipo_seguro', sa.Integer(), nullable=False),
        sa.Column('Carpeta', sa.String(100), nullable=False),
        sa.Column('Poliza', sa.String(100), nullable=True),
        sa.Column('Endoso', sa.String(100), nullable=True),
        sa.Column('Vto_Desde', sa.Date(), nullable=False),
        sa.Column('Vto_Hasta', sa.Date(), nullable=False),
        sa.Column('Moneda', sa.String(10), nullable=False),
        sa.Column('Premio', sa.Float(), nullable=True),
        sa.Column('Cuotas', sa.Integer(), nullable=True),
        sa.Column('Observaciones', sa.Text(), nullable=True)
    )
    
    # Crear foreign keys
    op.create_foreign_key(
        'fk_movimiento_cliente',
        'movimientos_vigencias', 'clientes',
        ['Cliente'], ['numero_cliente']
    )
    op.create_foreign_key(
        'fk_cliente_creador',
        'clientes', 'usuarios',
        ['creado_por_id'], ['id']
    )
    op.create_foreign_key(
        'fk_cliente_modificador',
        'clientes', 'usuarios',
        ['modificado_por_id'], ['id']
    )

def downgrade():
    op.drop_table('movimientos_vigencias')
    op.drop_table('clientes')
    op.drop_table('usuarios')
    op.execute("DROP SEQUENCE IF EXISTS cliente_numero_seq")
