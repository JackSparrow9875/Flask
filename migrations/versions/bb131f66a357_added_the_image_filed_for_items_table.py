"""added the image filed for Items table

Revision ID: bb131f66a357
Revises: c7dda35d5b28
Create Date: 2024-03-19 12:11:45.534821

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bb131f66a357'
down_revision = 'c7dda35d5b28'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.add_column(sa.Column('item_img', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.drop_column('item_img')

    # ### end Alembic commands ###
