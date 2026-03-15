"""create initial tables

Revision ID: 0000000000
Revises:
Create Date: 2026-03-15 00:00:00.000000
"""
from typing import Sequence, Union
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSONB
from alembic import op

revision: str = '0000000000'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.execute("DO $$ BEGIN CREATE TYPE userrole AS ENUM ('free', 'premium', 'admin'); EXCEPTION WHEN duplicate_object THEN null; END $$;")

    op.execute("""
        CREATE TABLE users (
            id UUID PRIMARY KEY,
            name VARCHAR NOT NULL,
            email VARCHAR NOT NULL UNIQUE,
            password_hash VARCHAR NOT NULL,
            role userrole NOT NULL DEFAULT 'free',
            birth_date DATE,
            terms_accepted_at TIMESTAMP,
            email_verified BOOLEAN NOT NULL DEFAULT false,
            email_verified_at TIMESTAMP
        )
    """)

    op.create_table('profiles',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False, unique=True),
        sa.Column('favorite_genres', ARRAY(sa.String()), server_default='{}'),
        sa.Column('favorite_movies', ARRAY(sa.String()), server_default='{}'),
        sa.Column('favorite_actors', ARRAY(sa.String()), server_default='{}'),
        sa.Column('favorite_directors', ARRAY(sa.String()), server_default='{}'),
        sa.Column('language', sa.String(), nullable=False, server_default='pt'),
        sa.Column('country', sa.String(2), nullable=False, server_default='BR'),
        sa.Column('streaming_platforms', ARRAY(sa.String()), nullable=False, server_default='{}'),
    )

    op.create_table('recommendations',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, unique=True),
        sa.Column('prompt_used', sa.Text(), nullable=True),
        sa.Column('response', JSONB(), nullable=True),
        sa.Column('message', sa.Text(), nullable=True),
        sa.Column('language', sa.String(8), nullable=False, server_default='pt'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    op.create_table('password_reset_tokens',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('token', sa.String(64), unique=True, nullable=False),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.Column('used_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    op.create_table('email_verification_tokens',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('token', sa.String(64), unique=True, nullable=False, index=True),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.Column('used_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

def downgrade() -> None:
    op.drop_table('email_verification_tokens')
    op.drop_table('password_reset_tokens')
    op.drop_table('recommendations')
    op.drop_table('profiles')
    op.drop_table('users')
    op.execute("DROP TYPE userrole")
