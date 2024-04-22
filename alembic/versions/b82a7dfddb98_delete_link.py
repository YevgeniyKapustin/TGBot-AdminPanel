"""delete link

Revision ID: b82a7dfddb98
Revises: 02d5940ff177
Create Date: 2024-04-22 14:33:40.168129

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'b82a7dfddb98'
down_revision: Union[str, None] = '02d5940ff177'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('channel', 'link')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('channel', sa.Column('link', mysql.VARCHAR(length=256), nullable=False))
    # ### end Alembic commands ###
