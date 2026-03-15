"""add_language_to_recommendations

Revision ID: a3f92c1d0e47
Revises: 9fc8046827f8
Create Date: 2026-03-14 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'a3f92c1d0e47'
down_revision: Union[str, None] = '9fc8046827f8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    result = conn.execute(sa.text(
        "SELECT column_name FROM information_schema.columns WHERE table_name='recommendations' AND column_name='language'"
    ))
    if result.fetchone() is None:
        op.add_column('recommendations', sa.Column('language', sa.String(8), server_default='pt', nullable=False))


def downgrade() -> None:
    op.drop_column('recommendations', 'language')
