import sqlalchemy as sa
from sqlalchemy import ForeignKey

metadata = sa.MetaData()


User = sa.Table(
    'user',
    metadata,
    sa.Column('id', sa.Text, primary_key=True),
    sa.Column('username', sa.Text, nullable=False),
    sa.Column('email', sa.Text, nullable=False, unique=True),
    sa.Column('password', sa.Text, nullable=False),
    sa.Column('number', sa.Integer, nullable=False, unique=True),
    sa.Column('token', sa.Text, nullable=True)
)

Session = sa.Table(
    'session',
    metadata,
    sa.Column('id', sa.Text, primary_key=True),
    sa.Column('user_id', sa.Text, ForeignKey('user.id'), nullable=False),
    sa.Column('status', sa.Integer, nullable=False),
    sa.Column('total_score', sa.Integer, nullable=False),
    sa.Column('current_stage', sa.Integer, nullable=False),
    sa.Column('difficulty', sa.Integer, nullable=False),
    sa.Column('started_at', sa.DateTime, nullable=False)
)
