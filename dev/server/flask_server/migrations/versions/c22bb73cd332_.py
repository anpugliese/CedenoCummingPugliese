"""empty message

Revision ID: c22bb73cd332
Revises: a44b21021c72
Create Date: 2021-02-07 21:32:08.731519

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c22bb73cd332'
down_revision = 'a44b21021c72'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Waiting', sa.Column('enter_time', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Waiting', 'enter_time')
    # ### end Alembic commands ###
