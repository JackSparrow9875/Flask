"""corrected the tables

Revision ID: c7dda35d5b28
Revises: cb27ba30d459
Create Date: 2024-03-17 03:33:44.062507

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c7dda35d5b28'
down_revision = 'cb27ba30d459'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('category', schema=None) as batch_op:
        batch_op.drop_column('date_added')
        batch_op.drop_column('available')

    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_added', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('available', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.drop_column('available')
        batch_op.drop_column('date_added')

    with op.batch_alter_table('category', schema=None) as batch_op:
        batch_op.add_column(sa.Column('available', sa.BOOLEAN(), nullable=True))
        batch_op.add_column(sa.Column('date_added', sa.DATETIME(), nullable=True))

    # ### end Alembic commands ###