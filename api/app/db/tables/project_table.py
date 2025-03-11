import uuid

from sqlalchemy import BOOLEAN, TIMESTAMP, UUID, VARCHAR, Column

from app.db.dao.base_dao import BaseDAO
from app.db.database import BaseTable, Reflected


class Project(Reflected, BaseTable, BaseDAO):
    __tablename__ = 'project'

    uuid = Column(
        'UUID',
        UUID(as_uuid=True),
        nullable=False,
        default=uuid.uuid4,
        primary_key=True,
    )
    name = Column('NAME', VARCHAR, nullable=False)
    created_at = Column('CREATED_AT', TIMESTAMP(timezone=True), nullable=False)
    updated_at = Column('UPDATED_AT', TIMESTAMP(timezone=True), nullable=False)
    deleted = Column('DELETED', BOOLEAN, nullable=False, default=False)
