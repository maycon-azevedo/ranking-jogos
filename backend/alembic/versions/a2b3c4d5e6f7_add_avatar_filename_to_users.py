"""add avatar_filename to users

Revision ID: a2b3c4d5e6f7
Revises: f8a1732455c3
Create Date: 2026-06-14 01:00:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'a2b3c4d5e6f7'
down_revision: Union[str, None] = 'f8a1732455c3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('avatar_filename', sa.String(255), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'avatar_filename')
