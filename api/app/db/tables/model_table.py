import uuid

from sqlalchemy import BOOLEAN, INTEGER, TIMESTAMP, UUID, VARCHAR, Column

from app.db.dao.base_dao import BaseDAO
from app.db.database import BaseTable, Reflected
from app.db.tables.commons.json_encoded_dict import JSONEncodedDict


class Model(Reflected, BaseTable, BaseDAO):
    __tablename__ = 'model'

    id = Column('ID', INTEGER, primary_key=True)
    uuid = Column(
        'UUID', UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4
    )
    name = Column('NAME', VARCHAR, nullable=False)
    description = Column('DESCRIPTION', VARCHAR, nullable=True)
    model_type = Column('MODEL_TYPE', VARCHAR, nullable=False)
    data_type = Column('DATA_TYPE', VARCHAR, nullable=False)
    granularity = Column('GRANULARITY', VARCHAR, nullable=False)
    features = Column('FEATURES', JSONEncodedDict, nullable=True)
    outputs = Column('OUTPUTS', JSONEncodedDict, nullable=True)
    target = Column('TARGET', JSONEncodedDict, nullable=True)
    timestamp = Column('TIMESTAMP', JSONEncodedDict, nullable=True)
    frameworks = Column('FRAMEWORKS', VARCHAR, nullable=True)
    algorithm = Column('ALGORITHM', VARCHAR, nullable=True)
    created_at = Column('CREATED_AT', TIMESTAMP(timezone=True), nullable=False)
    updated_at = Column('UPDATED_AT', TIMESTAMP(timezone=True), nullable=False)
    deleted = Column('DELETED', BOOLEAN, nullable=False, default=False)
