from yarn_plugin.recommendations.application.query.get_pattern_recommendations.query import (
    GetPatternRecommendationsQuery,
)
from yarn_plugin.recommendations.application.query.get_pattern_recommendations.response import (
    GetPatternRecommendationsResponse,
    PatternDto,
)
from yarn_plugin.recommendations.domain.repository.pattern_repository_interface import (
    PatternRepositoryInterface,
)


class GetPatternRecommendationsHandler:
    def __init__(self, repository: PatternRepositoryInterface) -> None:
        self._repository = repository

    async def handle(self, query: GetPatternRecommendationsQuery) -> GetPatternRecommendationsResponse:
        patterns = await self._repository.search(query.query_text, query.limit)

        dtos = tuple(
            PatternDto(
                id=pattern.id,
                name=pattern.name,
                brand_id=pattern.brand_id,
                difficulty=pattern.difficulty,
                yarn_weight=pattern.yarn_weight,
                category=pattern.category,
                language=pattern.language,
                needle_size=pattern.needle_size,
                recommended_yarn_id=pattern.recommended_yarn_id,
                popularity_rating=pattern.popularity_rating,
                description=pattern.description,
                tags=tuple(pattern.tags),
            )
            for pattern in patterns
        )

        message = (
            f"Found {len(dtos)} pattern{'s' if len(dtos) != 1 else ''} matching your query."
            if dtos
            else "No patterns found matching your query. Try different keywords."
        )

        return GetPatternRecommendationsResponse(results=dtos, total=len(dtos), message=message)
