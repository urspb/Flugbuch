"""public_entries added to users table

Revision ID: 8539eeb03436
Revises: 834b1a697901
Create Date: 2022-05-16 21:17:11.769951

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8539eeb03436'
down_revision = '834b1a697901'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('public_entries', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'public_entries')
    # ### end Alembic commands ###