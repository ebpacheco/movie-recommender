"""add role to users

Revision ID: fca41f860268
Revises: 
Create Date: 2026-03-10 11:27:26.734273

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'fca41f860268'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column(
        'role',
        sa.Enum('free', 'premium', 'admin', name='userrole'),
        nullable=False,
        server_default='free',   # usuários existentes viram 'free'
    ))

    # Seta seu usuário como admin
    op.execute("UPDATE users SET role = 'admin' WHERE email = 'eduardobertoncinip@gmail.com'")


def downgrade() -> None:
    op.drop_column('users', 'role')
    sa.Enum(name='userrole').drop(op.get_bind(), checkfirst=True)