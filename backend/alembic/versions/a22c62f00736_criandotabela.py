"""criandoTabela

Revision ID: a22c62f00736
Revises: 
Create Date: 2025-07-10 21:42:13.449420
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from mercearia.api.security import get_password_hash
import uuid

# revision identifiers, used by Alembic.
revision: str = 'a22c62f00736'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'favoritos',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('produto_id', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'produtos',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('nome', sa.String(), nullable=False),
        sa.Column('descricao', sa.String(), nullable=False),
        sa.Column('preco', sa.Float(), nullable=False),
        sa.Column('imagem', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'users',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('role', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
        DELETE FROM users WHERE email IN ('admin@admin.com', 'jucelinofreitas@gmail.com')
    """)
    op.execute("""
        DELETE FROM produtos WHERE id IN ('1', '2', '3', '4')
    """)
    op.drop_table('users')
    op.drop_table('produtos')
    op.drop_table('favoritos')
