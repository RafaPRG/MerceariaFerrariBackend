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

    # Inserir usuário admin
    admin_id = str(uuid.uuid4())
    hashed_password_admin = get_password_hash("Admin123!")
    op.execute(f"""
        INSERT INTO users (id, name, email, password, role)
        VALUES ('{admin_id}', 'Admin', 'admin@admin.com', '{hashed_password_admin}', 'admin')
    """)

    # Inserir usuário comum
    user_id = str(uuid.uuid4())
    hashed_password_user = get_password_hash("Juice123")
    op.execute(f"""
        INSERT INTO users (id, name, email, password, role)
        VALUES ('{user_id}', 'Jucelino Freitas', 'jucelinofreitas@gmail.com', '{hashed_password_user}', 'user')
    """)

    # Inserir produtos
    produtos = [
        {
            "id": "1",
            "nome": "Arroz",
            "descricao": "Arroz branco tipo 1",
            "preco": 5.99,
            "imagem": "arroz.jpg"
        },
        {
            "id": "2",
            "nome": "Feijão",
            "descricao": "Feijão carioca",
            "preco": 6.49,
            "imagem": "feijao.jpg"
        },
        {
            "id": "3",
            "nome": "Macarrão",
            "descricao": "Macarrão espaguete",
            "preco": 4.99,
            "imagem": "macarrao.jpg"
        },
        {
            "id": "4",
            "nome": "Café",
            "descricao": "Café torrado e moído",
            "preco": 10.99,
            "imagem": "cafe.jpg"
        },
    ]

    for produto in produtos:
        op.execute(f"""
            INSERT INTO produtos (id, nome, descricao, preco, imagem)
            VALUES ('{produto["id"]}', '{produto["nome"]}', '{produto["descricao"]}', {produto["preco"]}, '{produto["imagem"]}')
        """)


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
