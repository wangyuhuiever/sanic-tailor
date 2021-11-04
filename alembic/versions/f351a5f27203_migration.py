"""migration

Revision ID: f351a5f27203
Revises: 
Create Date: 2021-11-04 15:54:01.722307

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f351a5f27203'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('create_date', sa.DateTime(), nullable=False),
    sa.Column('write_date', sa.DateTime(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('create_uid', sa.BigInteger(), nullable=True),
    sa.Column('write_uid', sa.BigInteger(), nullable=True),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['create_uid'], ['users.id'], ),
    sa.ForeignKeyConstraint(['write_uid'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone')
    )
    op.create_table('demo_model',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('create_date', sa.DateTime(), nullable=False),
    sa.Column('write_date', sa.DateTime(), nullable=False),
    sa.Column('create_uid', sa.BigInteger(), nullable=True),
    sa.Column('write_uid', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['create_uid'], ['users.id'], ),
    sa.ForeignKeyConstraint(['write_uid'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('demo_model')
    op.drop_table('users')
    # ### end Alembic commands ###
