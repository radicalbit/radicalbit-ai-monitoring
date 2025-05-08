from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from app.models.job_status import JobStatus


class Coordinate(BaseModel):
    x: float
    y: float


class EmbeddingsValue(BaseModel):
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

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )


class Histogram(BaseModel):
    buckets: List[float]
    reference_values: List[int]
    current_values: Optional[List[int]] = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )


class DriftScore(BaseModel):
    current_timestamp: str
    score: float

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    @staticmethod
    def from_raw(date: datetime, score: float) -> 'DriftScore':
        return DriftScore(
            current_timestamp=date.isoformat(),
            score=score,
        )


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
        drift_score: Optional[DriftScore],
    ) -> 'EmbeddingsReportDTO':
        """Create a EmbeddingsReportDTO from a dictionary of data."""
        embeddings = EmbeddingsReportDTO._create_embeddings(
            embeddings_data=embeddings_data
        )

        if drift_score:
            embeddings.drift_score = drift_score

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


class EmbeddingsDriftDTO(BaseModel):
    average_drift_score: float
    last_drift_score: DriftScore
    drift_scores: List[DriftScore]

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    @staticmethod
    def from_drift_scores(drift_scores: List[DriftScore]) -> 'EmbeddingsDriftDTO':
        """Create a EmbeddingsDriftDTO from a drift scores."""
        average_score = sum(ds.score for ds in drift_scores) / len(drift_scores)
        last_score = max(drift_scores, key=lambda ds: ds.current_timestamp)

        return EmbeddingsDriftDTO(
            average_drift_score=average_score,
            last_drift_score=last_score,
            drift_scores=drift_scores,
        )
