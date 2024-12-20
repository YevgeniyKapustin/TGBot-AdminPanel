"""add geo

Revision ID: 8bf6eebfe636
Revises: f265d4f41fe9
Create Date: 2024-05-22 11:39:53.432764

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8bf6eebfe636'
down_revision: Union[str, None] = 'f265d4f41fe9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('geo',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(length=256), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('geo')
    # ### end Alembic commands ###
