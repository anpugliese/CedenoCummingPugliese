"""empty message

Revision ID: 5cb5355daca2
Revises: 
Create Date: 2021-02-06 22:02:18.623704

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5cb5355daca2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Waiting', sa.Column('wait_time', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Waiting', 'wait_time')
    # ### end Alembic commands ###
