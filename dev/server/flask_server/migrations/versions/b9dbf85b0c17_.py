"""empty message

Revision ID: b9dbf85b0c17
Revises: 57c05f96e9aa
Create Date: 2021-02-04 20:40:25.125156

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'b9dbf85b0c17'
down_revision = '57c05f96e9aa'
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
    op.drop_table('Request')
    op.drop_table('Section')
    op.add_column('Shopping', sa.Column('token', sa.String(), nullable=False))
    op.create_unique_constraint(None, 'Shopping', ['username'])
    op.drop_column('Shopping', 'request_id')
    op.add_column('Waiting', sa.Column('req_time', sa.DateTime(), nullable=False))
    op.add_column('Waiting', sa.Column('shop_time', sa.DateTime(), nullable=False))
    op.add_column('Waiting', sa.Column('token', sa.String(), nullable=False))
    op.create_unique_constraint(None, 'Waiting', ['username'])
    op.drop_column('Waiting', 'request_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Waiting', sa.Column('request_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'Waiting', type_='unique')
    op.drop_column('Waiting', 'token')
    op.drop_column('Waiting', 'shop_time')
    op.drop_column('Waiting', 'req_time')
    op.add_column('Shopping', sa.Column('request_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'Shopping', type_='unique')
    op.drop_column('Shopping', 'token')
    op.create_table('Section',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"Section_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('max_capacity', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='Section_pkey'),
    sa.UniqueConstraint('name', name='Section_name_key')
    )
    op.create_table('Request',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"Request_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('supermarket_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('time', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('type_id', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='Request_pkey')
    )
    op.drop_table('Record')
    # ### end Alembic commands ###
