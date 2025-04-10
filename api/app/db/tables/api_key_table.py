from sqlalchemy import TIMESTAMP, UUID, VARCHAR, Column, ForeignKey

from app.db.dao.base_dao import BaseDAO
from app.db.database import BaseTable, Reflected


class ApiKey(Reflected, BaseTable, BaseDAO):
    __tablename__ = 'api_key'

    name = Column('NAME', VARCHAR(), nullable=False, primary_key=True)
    project_uuid = Column(
        'PROJECT_UUID',
        UUID(),
        ForeignKey('project.UUID', ondelete='CASCADE'),
        nullable=False,
        primary_key=True,
    )
    hashed_key = Column('HASHED_KEY', VARCHAR(128), nullable=False)
    obscured_key = Column('OBSCURED_KEY', VARCHAR(128), nullable=False)
    created_at = Column('CREATED_AT', TIMESTAMP(timezone=True), nullable=False)
    updated_at = Column('UPDATED_AT', TIMESTAMP(timezone=True), nullable=False)
