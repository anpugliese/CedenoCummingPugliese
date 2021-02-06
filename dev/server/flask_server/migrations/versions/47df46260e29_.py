"""empty message

Revision ID: 47df46260e29
Revises: 668ba9433f39
Create Date: 2021-02-04 07:41:15.815525

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '47df46260e29'
down_revision = '668ba9433f39'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Waiting', sa.Column('req_time', sa.DateTime(), nullable=False))
    op.add_column('Waiting', sa.Column('shop_time', sa.DateTime(), nullable=False))
    op.drop_column('Waiting', 'date_time')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Waiting', sa.Column('date_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    op.drop_column('Waiting', 'shop_time')
    op.drop_column('Waiting', 'req_time')
    # ### end Alembic commands ###