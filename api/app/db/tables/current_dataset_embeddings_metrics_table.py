from uuid import uuid4

from sqlalchemy import UUID, Column, ForeignKey

from app.db.dao.base_dao import BaseDAO
from app.db.database import BaseTable, Reflected
from app.db.tables.commons.json_encoded_dict import JSONEncodedDict


class CurrentDatasetEmbeddingsMetrics(Reflected, BaseTable, BaseDAO):
    __tablename__ = 'current_dataset_embeddings_metrics'

    uuid = Column(
        'UUID',
        UUID(as_uuid=True),
        nullable=False,
        default=uuid4,
        primary_key=True,
    )
    current_uuid = Column(
        'CURRENT_UUID',
        UUID(as_uuid=True),
        ForeignKey('current_dataset.UUID'),
        nullable=False,
    )
    metrics = Column('METRICS', JSONEncodedDict, nullable=True)
    drift = Column('DRIFT', JSONEncodedDict, nullable=True)
