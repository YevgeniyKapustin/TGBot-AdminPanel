"""add userbot

Revision ID: 02d5940ff177
Revises: b49026a05427
Create Date: 2024-04-21 09:20:48.104874

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '02d5940ff177'
down_revision: Union[str, None] = 'b49026a05427'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('userbot',
    sa.Column('phone', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('phone')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('userbot')
    # ### end Alembic commands ###