from uuid import uuid4

from sqlalchemy import TIMESTAMP, UUID, VARCHAR, Column, ForeignKey

from app.db.dao.base_dao import BaseDAO
from app.db.database import BaseTable, Reflected
from app.models.job_status import JobStatus


class CompletionDataset(Reflected, BaseTable, BaseDAO):
    __tablename__ = 'completion_dataset'

    uuid = Column(
        'UUID',
        UUID(as_uuid=True),
        nullable=False,
        default=uuid4,
        primary_key=True,
    )
    model_uuid = Column(
        'MODEL_UUID', UUID(as_uuid=True), ForeignKey('model.UUID'), nullable=False
    )
    path = Column('PATH', VARCHAR, nullable=False)
    date = Column('DATE', TIMESTAMP(timezone=True), nullable=False)
    status = Column('STATUS', VARCHAR, nullable=False, default=JobStatus.IMPORTING)
