"""add_dataset_and_metrics_completion

Revision ID: e72dc7aaa4cc
Revises: dccb82489f4d
Create Date: 2024-12-11 13:33:38.759485

"""
from typing import Sequence, Union, Text

from alembic import op
import sqlalchemy as sa
from app.db.tables.commons.json_encoded_dict import JSONEncodedDict

# revision identifiers, used by Alembic.
revision: str = 'e72dc7aaa4cc'
down_revision: Union[str, None] = 'dccb82489f4d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('completion_dataset',
    sa.Column('UUID', sa.UUID(), nullable=False),
    sa.Column('MODEL_UUID', sa.UUID(), nullable=False),
    sa.Column('PATH', sa.VARCHAR(), nullable=False),
    sa.Column('DATE', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('STATUS', sa.VARCHAR(), nullable=False),
    sa.ForeignKeyConstraint(['MODEL_UUID'], ['model.UUID'], name=op.f('fk_completion_dataset_MODEL_UUID_model')),
    sa.PrimaryKeyConstraint('UUID', name=op.f('pk_completion_dataset'))
    )
    op.create_table('completion_dataset_metrics',
    sa.Column('UUID', sa.UUID(), nullable=False),
    sa.Column('COMPLETION_UUID', sa.UUID(), nullable=False),
    sa.Column('MODEL_QUALITY', JSONEncodedDict(astext_type=Text()), nullable=True),
    sa.ForeignKeyConstraint(['COMPLETION_UUID'], ['completion_dataset.UUID'], name=op.f('fk_completion_dataset_metrics_COMPLETION_UUID_completion_dataset')),
    sa.PrimaryKeyConstraint('UUID', name=op.f('pk_completion_dataset_metrics'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('completion_dataset_metrics')
    op.drop_table('completion_dataset')
    # ### end Alembic commands ###