"""Add username for users

Revision ID: 55ec2a0d42ff
Revises: c8037c1d6d6c
Create Date: 2019-04-18 02:23:13.439979

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '55ec2a0d42ff'
down_revision = 'c8037c1d6d6c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('username', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'username')
    # ### end Alembic commands ###
