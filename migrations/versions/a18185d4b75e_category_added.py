"""Category added

Revision ID: a18185d4b75e
Revises: 5a03df011696
Create Date: 2020-07-05 14:43:55.968038

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a18185d4b75e'
down_revision = '5a03df011696'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.add_column('post', sa.Column('category_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'post', 'category', ['category_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'post', type_='foreignkey')
    op.drop_column('post', 'category_id')
    op.drop_table('category')
    # ### end Alembic commands ###
