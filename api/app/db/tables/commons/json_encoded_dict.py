from sqlalchemy import TypeDecorator
from sqlalchemy.dialects.postgresql import JSONB


class JSONEncodedDict(TypeDecorator):
    impl = JSONB
    cache_ok = True

    def process_bind_param(self, value, dialect):
        return value

    def process_result_value(self, value, dialect):
        return value
