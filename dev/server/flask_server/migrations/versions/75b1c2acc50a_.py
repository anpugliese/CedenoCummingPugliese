"""empty message

Revision ID: 75b1c2acc50a
Revises: 57c05f96e9aa
Create Date: 2021-02-04 22:12:25.036130

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '75b1c2acc50a'
down_revision = 'b9dbf85b0c17'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Supermarket',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('address', sa.String(), nullable=True),
    sa.Column('logo', sa.String(), nullable=True),
    sa.Column('lat', sa.Float(), nullable=False),
    sa.Column('lon', sa.Float(), nullable=False),
    sa.Column('max_capacity', sa.Integer(), nullable=False),
    sa.Column('timetable', sa.JSON(), nullable=False),
    sa.Column('waiting_time', sa.Integer(), server_default='0', nullable=False),
    sa.Column('mean_shopping_time', sa.Integer(), server_default='10', nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Supermarket')
    # ### end Alembic commands ###