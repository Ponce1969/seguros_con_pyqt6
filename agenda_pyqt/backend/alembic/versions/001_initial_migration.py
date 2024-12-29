"""Initial migration

Revision ID: 001_initial_migration
Revises: 
Create Date: 2024-12-29 01:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001_initial_migration'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create users table
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=64), nullable=False),
        sa.Column('email', sa.String(length=64), nullable=False),
        sa.Column('password', sa.String(length=128), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=True, default=True),
        sa.Column('role', sa.String(length=20), nullable=True, default='user'),
        sa.Column('comision_porcentaje', sa.Float(), nullable=True, default=0.0),
        sa.Column('fecha_creacion', sa.DateTime(), nullable=True),
        sa.Column('ultima_modificacion', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )

    # Create corredores table
    op.create_table('corredores',
        sa.Column('numero', sa.Integer(), nullable=False),
        sa.Column('nombres', sa.String(length=30), nullable=True),
        sa.Column('apellidos', sa.String(length=30), nullable=False),
        sa.Column('documento', sa.String(length=20), nullable=False),
        sa.Column('direccion', sa.String(length=70), nullable=False),
        sa.Column('localidad', sa.String(length=15), nullable=False),
        sa.Column('telefonos', sa.String(length=15), nullable=True),
        sa.Column('movil', sa.String(length=15), nullable=True),
        sa.Column('mail', sa.String(length=40), nullable=False),
        sa.Column('observaciones', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('numero'),
        sa.UniqueConstraint('documento')
    )

    # Create tipos_de_seguros table
    op.create_table('tipos_de_seguros',
        sa.Column('id_tipo', sa.Integer(), nullable=False),
        sa.Column('aseguradora', sa.String(length=15), nullable=False),
        sa.Column('codigo', sa.String(length=5), nullable=False),
        sa.Column('descripcion', sa.String(length=30), nullable=False),
        sa.PrimaryKeyConstraint('id_tipo')
    )

    # Create clientes table
    op.create_table('clientes',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('nombres', sa.String(length=30), nullable=False),
        sa.Column('apellidos', sa.String(length=30), nullable=False),
        sa.Column('tipo_documento', sa.String(length=4), nullable=False),
        sa.Column('documentos', sa.String(length=20), nullable=False),
        sa.Column('fecha_nacimiento', sa.Date(), nullable=False),
        sa.Column('direccion', sa.String(length=70), nullable=False),
        sa.Column('localidad', sa.String(length=15), nullable=True),
        sa.Column('telefonos', sa.String(length=20), nullable=False),
        sa.Column('movil', sa.String(length=20), nullable=False),
        sa.Column('mail', sa.String(length=50), nullable=False),
        sa.Column('corredor', sa.Integer(), nullable=True),
        sa.Column('observaciones', sa.Text(), nullable=True),
        sa.Column('creado_por_id', sa.Integer(), nullable=False),
        sa.Column('modificado_por_id', sa.Integer(), nullable=False),
        sa.Column('fecha_creacion', sa.DateTime(), nullable=True),
        sa.Column('fecha_modificacion', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['creado_por_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['modificado_por_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create movimientos_vigencias table
    op.create_table('movimientos_vigencias',
        sa.Column('id_movimiento', sa.Integer(), nullable=False),
        sa.Column('fecha_mov', sa.Date(), nullable=False),
        sa.Column('corredor', sa.Integer(), nullable=False),
        sa.Column('cliente_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('numero_cliente_compania', sa.String(), nullable=True),
        sa.Column('tipo_seguro', sa.Integer(), nullable=False),
        sa.Column('carpeta', sa.String(), nullable=False),
        sa.Column('poliza', sa.String(), nullable=True),
        sa.Column('endoso', sa.String(), nullable=True),
        sa.Column('vto_desde', sa.Date(), nullable=False),
        sa.Column('vto_hasta', sa.Date(), nullable=False),
        sa.Column('moneda', sa.String(), nullable=False),
        sa.Column('premio', sa.Float(), nullable=True),
        sa.Column('cuotas', sa.Integer(), nullable=True),
        sa.Column('observaciones', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['cliente_id'], ['clientes.id'], ),
        sa.ForeignKeyConstraint(['corredor'], ['corredores.numero'], ),
        sa.ForeignKeyConstraint(['tipo_seguro'], ['tipos_de_seguros.id_tipo'], ),
        sa.PrimaryKeyConstraint('id_movimiento')
    )

    # Create indexes
    op.create_index(op.f('ix_clientes_documentos'), 'clientes', ['documentos'], unique=True)
    op.create_index(op.f('ix_clientes_mail'), 'clientes', ['mail'], unique=True)
    op.create_index(op.f('ix_clientes_id'), 'clientes', ['id'], unique=False)


def downgrade() -> None:
    op.drop_table('movimientos_vigencias')
    op.drop_table('clientes')
    op.drop_table('tipos_de_seguros')
    op.drop_table('corredores')
    op.drop_table('users')
