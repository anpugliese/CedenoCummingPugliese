"""empty message

Revision ID: 8c534a96fe67
Revises: df7fd0ea7643
Create Date: 2021-01-29 16:08:12.516949

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8c534a96fe67'
down_revision = 'df7fd0ea7643'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Supermarket', 'address',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Supermarket', 'address',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###