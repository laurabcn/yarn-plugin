from dataclasses import dataclass


@dataclass(frozen=True)
class GetYarnRecommendationsQuery:
    query_text: str
    limit: int = 5