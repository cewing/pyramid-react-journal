"""add user apikey

Revision ID: 7e3d4d6e7e68
Revises: 10ddb8272415
Create Date: 2016-03-22 19:56:12.018106

"""

# revision identifiers, used by Alembic.
revision = '7e3d4d6e7e68'
down_revision = '10ddb8272415'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


def upgrade():
    op.add_column(
        'users', sa.Column('key', postgresql.UUID(as_uuid=True), nullable=True)
    )


def downgrade():
    op.drop_column('users', 'key')
