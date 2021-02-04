"""empty message

Revision ID: 57c05f96e9aa
Revises: 
Create Date: 2021-02-04 19:25:40.633606

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '57c05f96e9aa'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Record',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('enter_time', sa.DateTime(), nullable=False),
    sa.Column('exit_time', sa.DateTime(), nullable=False),
    sa.Column('supermarket_id', sa.Integer(), nullable=False),
    sa.Column('delta_time', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Shopping',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('token', sa.String(), nullable=False),
    sa.Column('supermarket_id', sa.Integer(), nullable=False),
    sa.Column('enter_time', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('Waiting',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('token', sa.String(), nullable=False),
    sa.Column('supermarket_id', sa.Integer(), nullable=False),
    sa.Column('req_time', sa.DateTime(), nullable=False),
    sa.Column('shop_time', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Waiting')
    op.drop_table('Shopping')
    op.drop_table('Record')
    # ### end Alembic commands ###
