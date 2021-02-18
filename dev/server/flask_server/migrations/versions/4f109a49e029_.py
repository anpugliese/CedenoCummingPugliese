"""empty message

Revision ID: 4f109a49e029
Revises: d065416ca11e
Create Date: 2021-02-07 14:52:07.470404

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4f109a49e029'
down_revision = 'd065416ca11e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Waiting', sa.Column('type_id', sa.Integer(), nullable=True))
    op.alter_column('Waiting', 'wait_time',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Waiting', 'wait_time',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_column('Waiting', 'type_id')
    # ### end Alembic commands ###