"""empty message

Revision ID: 2972d606a134
Revises: 1a1a46b3fc1f
Create Date: 2022-11-30 21:57:14.362285

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2972d606a134'
down_revision = '1a1a46b3fc1f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('question', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=False,
               existing_server_default=sa.text("'1'"))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('question', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=True,
               existing_server_default=sa.text("'1'"))

    # ### end Alembic commands ###