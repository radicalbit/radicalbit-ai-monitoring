from clickhouse_sqlalchemy.engines import MergeTree
from clickhouse_sqlalchemy.types import Array, DateTime64, LowCardinality, Map
from sqlalchemy import BigInteger, Column, String, func

from app.db.database import ClickHouseBaseTable


class Traces(ClickHouseBaseTable):
    __tablename__ = 'otel_traces'

    __table_args__ = (
        MergeTree(
            partition_by=func.toDate('Timestamp'),
            order_by=('ServiceName', 'SpanName', 'Timestamp'),
            index_granularity=8192,
            ttl_only_drop_parts=1,
        ),
    )
    timestamp = Column('Timestamp', DateTime64(9), primary_key=True)
    trace_id = Column('TraceId', String)
    span_id = Column('SpanId', String)
    parent_span_id = Column('ParentSpanId', String)
    trace_state = Column('TraceState', String)
    span_name = Column('SpanName', LowCardinality(String), primary_key=True)
    span_kind = Column('SpanKind', LowCardinality(String))
    service_name = Column('ServiceName', LowCardinality(String), primary_key=True)
    resource_attributes = Column(
        'ResourceAttributes', Map(LowCardinality(String), String)
    )
    scope_name = Column('ScopeName', String)
    scope_version = Column('ScopeVersion', String)
    span_attributes = Column('SpanAttributes', Map(LowCardinality(String), String))
    duration = Column('Duration', BigInteger)
    status_code = Column('StatusCode', LowCardinality(String))
    status_message = Column('StatusMessage', String)
    event_timestamp = Column('Events.Timestamp', Array(DateTime64(9)))
    events_name = Column('Events.Name', Array(LowCardinality(String)))
    events_attributes = Column(
        'Events.Attributes', Array(Map(LowCardinality(String), String))
    )
    links_trace_id = Column('Links.TraceId', Array(String))
    links_span_id = Column('Links.SpanId', Array(String))
    links_trace_state = Column('Links.TraceState', Array(String))
    links_attributes = Column(
        'Links.Attributes', Array(Map(LowCardinality(String), String))
    )
