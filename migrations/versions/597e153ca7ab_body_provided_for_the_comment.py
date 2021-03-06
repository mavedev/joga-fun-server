"""Body provided for the Comment

Revision ID: 597e153ca7ab
Revises: a18185d4b75e
Create Date: 2020-07-05 15:02:50.548885

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '597e153ca7ab'
down_revision = 'a18185d4b75e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comment', sa.Column('body', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('comment', 'body')
    # ### end Alembic commands ###
