"""Add db models

Revision ID: 77351761e057
Revises: 
Create Date: 2025-01-12 22:13:42.778986

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from geoalchemy2.types import Geometry
# revision identifiers, used by Alembic.
revision: str = '77351761e057'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('area_of_interest',
    sa.Column('file_name', sa.String(length=100), nullable=False),
    sa.Column('geometry', Geometry(from_text='ST_GeomFromEWKT', name='geometry', nullable=False), nullable=False),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('modified', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('projects',
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.Column('start_date', sa.Date(), nullable=False),
    sa.Column('end_date', sa.Date(), nullable=False),
    sa.Column('area_of_interest_id', sa.String(), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('modified', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['area_of_interest_id'], ['area_of_interest.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('projects')
    op.drop_index('idx_area_of_interest_geometry', table_name='area_of_interest', postgresql_using='gist')
    op.drop_table('area_of_interest')
