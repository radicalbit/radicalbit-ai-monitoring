from typing import List, Optional

from pydantic import BaseModel

from radicalbit_platform_sdk.models import ClassMetrics


class BinaryDistributionChartData(BaseModel):
    title: str
    reference_data: List[ClassMetrics]
    current_data: Optional[List[ClassMetrics]] = None
