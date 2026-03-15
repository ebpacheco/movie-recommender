"""add role to users

Revision ID: fca41f860268
Revises: 
Create Date: 2026-03-10 11:27:26.734273

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'fca41f860268'
down_revision: Union[str, None] = '0000000000'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(sa.text(
        "UPDATE users SET role = 'admin' WHERE email = 'eduardobertoncinip@gmail.com'"
    ))


def downgrade() -> None:
    pass