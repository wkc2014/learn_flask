"""empty message

Revision ID: f138a860d6b7
Revises: d0417da48687
Create Date: 2017-06-05 23:47:49.604000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f138a860d6b7'
down_revision = 'd0417da48687'
branch_labels = None
depends_on = None


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('articles', sa.Column('create_time', sa.DateTime(), nullable=True))
    op.add_column('articles', sa.Column('update_time', sa.DateTime(), nullable=True))
    op.drop_column('articles', 'timestamp')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('articles', sa.Column('timestamp', sa.DATETIME(), nullable=True))
    op.drop_column('articles', 'update_time')
    op.drop_column('articles', 'create_time')
    ### end Alembic commands ###
