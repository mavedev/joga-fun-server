"""Image URLs provided for posts

Revision ID: 289dabdd2a8a
Revises: 597e153ca7ab
Create Date: 2020-07-05 18:30:35.204358

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '289dabdd2a8a'
down_revision = '597e153ca7ab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('image_url', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'image_url')
    # ### end Alembic commands ###
