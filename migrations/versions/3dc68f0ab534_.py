"""empty message

Revision ID: 3dc68f0ab534
Revises: 619137aece7c
Create Date: 2019-04-26 11:55:01.896114

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3dc68f0ab534'
down_revision = '619137aece7c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('dish_categories', sa.Column('name_uz', sa.String(length=100), nullable=True))
    op.add_column('dishes', sa.Column('description_uz', sa.String(length=500), nullable=True))
    op.add_column('dishes', sa.Column('image_path', sa.String(), nullable=True))
    op.add_column('dishes', sa.Column('name_uz', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('dishes', 'name_uz')
    op.drop_column('dishes', 'image_path')
    op.drop_column('dishes', 'description_uz')
    op.drop_column('dish_categories', 'name_uz')
    # ### end Alembic commands ###
