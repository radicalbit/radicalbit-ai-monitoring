from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from app.models.job_status import JobStatus


class Coordinate(BaseModel):
    x: float
    y: float


class EmbeddingsValue(BaseModel):
    # timestamp: Optional[str] = None
    x: float
    y: float


class Embeddings(BaseModel):
    centroid: Coordinate
    values: List[EmbeddingsValue]


class EmbeddingsMetrics(BaseModel):
    n_comp: int
    n_cluster: int
    inertia: float
    sil_score: float


class Histogram(BaseModel):
    buckets: List[float]
    reference_values: List[int]
    current_values: Optional[List[int]] = None


class DriftScore(BaseModel):
    current_timestamp: str
    score: float


class EmbeddingsReport(BaseModel):
    reference_embeddings_metrics: EmbeddingsMetrics
    reference_embeddings: Embeddings
    current_embeddings_metrics: Optional[EmbeddingsMetrics] = None
    current_embeddings: Optional[Embeddings] = None
    histogram: Histogram
    drift_score: Optional[DriftScore] = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )


class EmbeddingsReportDTO(BaseModel):
    job_status: JobStatus
    embeddings: Optional[EmbeddingsReport]

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    @staticmethod
    def from_dict(
        job_status: JobStatus,
        embeddings_data: Optional[Dict],
    ) -> 'EmbeddingsReportDTO':
        """Create a EmbeddingsReportDTO from a dictionary of data."""
        embeddings = EmbeddingsReportDTO._create_embeddings(
            embeddings_data=embeddings_data
        )

        return EmbeddingsReportDTO(
            job_status=job_status,
            embeddings=embeddings,
        )

    @staticmethod
    def _create_embeddings(
        embeddings_data: Optional[Dict],
    ) -> Optional[EmbeddingsReport]:
        """Create an embeddings instance from a dictionary of data."""
        if not embeddings_data:
            return None
        return EmbeddingsReport(**embeddings_data)
