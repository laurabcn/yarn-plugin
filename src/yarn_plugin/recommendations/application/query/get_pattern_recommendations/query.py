from dataclasses import dataclass


@dataclass(frozen=True)
class GetPatternRecommendationsQuery:
    query_text: str
    limit: int = 5
