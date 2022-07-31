"""Tabellen Task, Message etc. entfernt

Revision ID: 063003705dc0
Revises: de8f7b8d0e36
Create Date: 2022-07-21 20:18:29.416140

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '063003705dc0'
down_revision = 'de8f7b8d0e36'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_message_timestamp', table_name='message')
    op.drop_table('message')
    op.drop_index('ix_task_name', table_name='task')
    op.drop_table('task')
    op.drop_index('ix_notification_name', table_name='notification')
    op.drop_index('ix_notification_timestamp', table_name='notification')
    op.drop_table('notification')
    op.drop_index('ix_user_username', table_name='user')
    op.drop_column('user', 'last_message_read_time')
    op.drop_column('user', 'username')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('username', sa.VARCHAR(length=64), nullable=True))
    op.add_column('user', sa.Column('last_message_read_time', sa.DATETIME(), nullable=True))
    op.create_index('ix_user_username', 'user', ['username'], unique=False)
    op.create_table('notification',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=128), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('timestamp', sa.FLOAT(), nullable=True),
    sa.Column('payload_json', sa.TEXT(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_notification_timestamp', 'notification', ['timestamp'], unique=False)
    op.create_index('ix_notification_name', 'notification', ['name'], unique=False)
    op.create_table('task',
    sa.Column('id', sa.VARCHAR(length=36), nullable=False),
    sa.Column('name', sa.VARCHAR(length=128), nullable=True),
    sa.Column('description', sa.VARCHAR(length=128), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('complete', sa.BOOLEAN(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_task_name', 'task', ['name'], unique=False)
    op.create_table('message',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('sender_id', sa.INTEGER(), nullable=True),
    sa.Column('recipient_id', sa.INTEGER(), nullable=True),
    sa.Column('body', sa.VARCHAR(length=140), nullable=True),
    sa.Column('timestamp', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['recipient_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['sender_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_message_timestamp', 'message', ['timestamp'], unique=False)
    # ### end Alembic commands ###