"""foreign

Revision ID: beefd9389835
Revises: a22c62f00736
Create Date: 2025-07-21 23:51:32.525948

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'beefd9389835'
down_revision: Union[str, Sequence[str], None] = 'a22c62f00736'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'favoritos', 'produtos', ['produto_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'favoritos', type_='foreignkey')
    # ### end Alembic commands ###
