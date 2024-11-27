"""new migration with upd names

Revision ID: a190b8aed674
Revises: 
Create Date: 2024-11-28 01:20:39.965961

"""
from alembic import op
import sqlalchemy as sa

from project.core.config import settings


# revision identifiers, used by Alembic.
revision = 'a190b8aed674'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
