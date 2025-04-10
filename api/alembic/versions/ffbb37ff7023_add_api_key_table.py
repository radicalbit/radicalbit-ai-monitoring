"""add api key table

Revision ID: ffbb37ff7023
Revises: 674d72dc789e
Create Date: 2025-04-01 16:50:17.382888

"""
from typing import Sequence, Union, Text

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ffbb37ff7023'
down_revision: Union[str, None] = '674d72dc789e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("api_key", 
        sa.Column('NAME', sa.VARCHAR(), nullable=False),
        sa.Column('PROJECT_UUID', sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(['PROJECT_UUID'], ['project.UUID'], name='fk_api_keys_project', ondelete='CASCADE'),
        sa.Column('HASHED_KEY', sa.String(128), nullable=False),
        sa.Column('OBSCURED_KEY', sa.String(128), nullable=False),
        sa.Column('CREATED_AT', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('UPDATED_AT', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("NAME", "PROJECT_UUID", name="pk_api_key"),
    )


def downgrade() -> None:
    op.drop_table('api_key')
