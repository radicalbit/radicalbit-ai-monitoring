from clickhouse_sqlalchemy.engines import MergeTree
from clickhouse_sqlalchemy.types import Array, DateTime64, LowCardinality, Map, Nested
from sqlalchemy import BigInteger, Column, String, func

from app.db.clickhouse_database import ClickHouseBaseTable


class Trace(ClickHouseBaseTable):
    __tablename__ = 'otel_traces'

    timestamp = Column('Timestamp', DateTime64(9))
    trace_id = Column('TraceId', String, primary_key=True)
    span_id = Column('SpanId', String, primary_key=True)
    parent_span_id = Column('ParentSpanId', String)
    trace_state = Column('TraceState', String)
    span_name = Column('SpanName', LowCardinality(String))
    span_kind = Column('SpanKind', LowCardinality(String))
    service_name = Column('ServiceName', LowCardinality(String))
    resource_attributes = Column(
        'ResourceAttributes', Map(LowCardinality(String), String)
    )
    scope_name = Column('ScopeName', String)
    scope_version = Column('ScopeVersion', String)
    span_attributes = Column('SpanAttributes', Map(LowCardinality(String), String))
    duration = Column('Duration', BigInteger)
    status_code = Column('StatusCode', LowCardinality(String))
    status_message = Column('StatusMessage', String)
    events = Column(
        'Events',
        Array(
            Nested(
                Column('Timestamp', DateTime64(9), key='timestamp'),
                Column('Name', LowCardinality(String), key='name'),
                Column(
                    'Attributes', Map(LowCardinality(String), String), key='attributes'
                ),
            )
        ),
        nullable=True,
    )
    links = Column(
        'Links',
        Array(
            Nested(
                Column('TraceId', String, key='trace_id'),
                Column('SpanId', String, key='span_id'),
                Column('TraceState', String, key='trace_state'),
                Column(
                    'Attributes', Map(LowCardinality(String), String), key='attributes'
                ),
            )
        ),
        nullable=True,
    )

    __table_args__ = (
        MergeTree(
            partition_by=func.toDate(timestamp),
            order_by=(service_name, span_name, func.toDateTime(timestamp)),
            index_granularity=8192,
            ttl_only_drop_parts=1,
        ),
    )
