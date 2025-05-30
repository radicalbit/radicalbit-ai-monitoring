"""init db

Revision ID: 6edab3f23907
Revises: 
Create Date: 2024-10-16 13:50:44.743062

"""
from typing import Sequence, Union, Text

from alembic import op
import sqlalchemy as sa
from app.db.tables.commons.json_encoded_dict import JSONEncodedDict

# revision identifiers, used by Alembic.
revision: str = '6edab3f23907'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('model',
    sa.Column('ID', sa.INTEGER(), nullable=False),
    sa.Column('UUID', sa.UUID(), nullable=False),
    sa.Column('NAME', sa.VARCHAR(), nullable=False),
    sa.Column('DESCRIPTION', sa.VARCHAR(), nullable=True),
    sa.Column('MODEL_TYPE', sa.VARCHAR(), nullable=False),
    sa.Column('DATA_TYPE', sa.VARCHAR(), nullable=False),
    sa.Column('GRANULARITY', sa.VARCHAR(), nullable=False),
    sa.Column('FEATURES', JSONEncodedDict(astext_type=Text()), nullable=True),
    sa.Column('OUTPUTS', JSONEncodedDict(astext_type=Text()), nullable=True),
    sa.Column('TARGET', JSONEncodedDict(astext_type=Text()), nullable=True),
    sa.Column('TIMESTAMP', JSONEncodedDict(astext_type=Text()), nullable=True),
    sa.Column('FRAMEWORKS', sa.VARCHAR(), nullable=True),
    sa.Column('ALGORITHM', sa.VARCHAR(), nullable=True),
    sa.Column('CREATED_AT', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('UPDATED_AT', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('DELETED', sa.BOOLEAN(), nullable=False),
    sa.PrimaryKeyConstraint('ID', name=op.f('pk_model')),
    sa.UniqueConstraint('UUID', name=op.f('uq_model_UUID'))
    )
    op.create_table('current_dataset',
    sa.Column('UUID', sa.UUID(), nullable=False),
    sa.Column('MODEL_UUID', sa.UUID(), nullable=False),
    sa.Column('PATH', sa.VARCHAR(), nullable=False),
    sa.Column('DATE', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('CORRELATION_ID_COLUMN', sa.VARCHAR(), nullable=True),
    sa.Column('STATUS', sa.VARCHAR(), nullable=False),
    sa.ForeignKeyConstraint(['MODEL_UUID'], ['model.UUID'], name=op.f('fk_current_dataset_MODEL_UUID_model')),
    sa.PrimaryKeyConstraint('UUID', name=op.f('pk_current_dataset'))
    )
    op.create_table('reference_dataset',
    sa.Column('UUID', sa.UUID(), nullable=False),
    sa.Column('MODEL_UUID', sa.UUID(), nullable=False),
    sa.Column('PATH', sa.VARCHAR(), nullable=False),
    sa.Column('DATE', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('STATUS', sa.VARCHAR(), nullable=False),
    sa.ForeignKeyConstraint(['MODEL_UUID'], ['model.UUID'], name=op.f('fk_reference_dataset_MODEL_UUID_model')),
    sa.PrimaryKeyConstraint('UUID', name=op.f('pk_reference_dataset'))
    )
    op.create_table('current_dataset_metrics',
    sa.Column('UUID', sa.UUID(), nullable=False),
    sa.Column('CURRENT_UUID', sa.UUID(), nullable=False),
    sa.Column('MODEL_QUALITY', JSONEncodedDict(astext_type=Text()), nullable=True),
    sa.Column('DATA_QUALITY', JSONEncodedDict(astext_type=Text()), nullable=True),
    sa.Column('DRIFT', JSONEncodedDict(astext_type=Text()), nullable=True),
    sa.Column('STATISTICS', JSONEncodedDict(astext_type=Text()), nullable=True),
    sa.ForeignKeyConstraint(['CURRENT_UUID'], ['current_dataset.UUID'], name=op.f('fk_current_dataset_metrics_CURRENT_UUID_current_dataset')),
    sa.PrimaryKeyConstraint('UUID', name=op.f('pk_current_dataset_metrics'))
    )
    op.create_table('reference_dataset_metrics',
    sa.Column('UUID', sa.UUID(), nullable=False),
    sa.Column('REFERENCE_UUID', sa.UUID(), nullable=False),
    sa.Column('MODEL_QUALITY', JSONEncodedDict(astext_type=Text()), nullable=True),
    sa.Column('DATA_QUALITY', JSONEncodedDict(astext_type=Text()), nullable=True),
    sa.Column('STATISTICS', JSONEncodedDict(astext_type=Text()), nullable=True),
    sa.ForeignKeyConstraint(['REFERENCE_UUID'], ['reference_dataset.UUID'], name=op.f('fk_reference_dataset_metrics_REFERENCE_UUID_reference_dataset')),
    sa.PrimaryKeyConstraint('UUID', name=op.f('pk_reference_dataset_metrics'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reference_dataset_metrics')
    op.drop_table('current_dataset_metrics')
    op.drop_table('reference_dataset')
    op.drop_table('current_dataset')
    op.drop_table('model')
    # ### end Alembic commands ###
