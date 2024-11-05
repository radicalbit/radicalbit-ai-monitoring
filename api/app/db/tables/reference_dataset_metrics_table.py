from uuid import uuid4

from sqlalchemy import UUID, Column, ForeignKey

from app.db.dao.base_dao import BaseDAO
from app.db.database import BaseTable, Reflected
from app.db.tables.commons.json_encoded_dict import JSONEncodedDict


class ReferenceDatasetMetrics(Reflected, BaseTable, BaseDAO):
    __tablename__ = 'reference_dataset_metrics'

    uuid = Column(
        'UUID',
        UUID(as_uuid=True),
        nullable=False,
        default=uuid4,
        primary_key=True,
    )
    reference_uuid = Column(
        'REFERENCE_UUID',
        UUID(as_uuid=True),
        ForeignKey('reference_dataset.UUID'),
        nullable=False,
    )
    model_quality = Column('MODEL_QUALITY', JSONEncodedDict, nullable=True)
    data_quality = Column('DATA_QUALITY', JSONEncodedDict, nullable=True)
    statistics = Column('STATISTICS', JSONEncodedDict, nullable=True)
