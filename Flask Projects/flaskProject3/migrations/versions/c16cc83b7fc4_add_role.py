"""add role

Revision ID: c16cc83b7fc4
Revises: 9510f6c2cd61
Create Date: 2024-05-16 19:23:47.184315

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c16cc83b7fc4'
down_revision = '9510f6c2cd61'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('permission', sa.Enum('USER', 'MODERATOR', 'ADMIN', name='permission'), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('permission')

    # ### end Alembic commands ###
