from yarn_plugin.recommendations.application.query.get_yarn_recommendations.query import GetYarnRecommendationsQuery
from yarn_plugin.recommendations.application.query.get_yarn_recommendations.response import (
    GetYarnRecommendationsResponse,
    YarnDto,
)
from yarn_plugin.recommendations.domain.repository.yarn_repository_interface import YarnRepositoryInterface


class GetYarnRecommendationsHandler:
    def __init__(self, repository: YarnRepositoryInterface) -> None:
        self._repository = repository

    async def handle(self, query: GetYarnRecommendationsQuery) -> GetYarnRecommendationsResponse:
        yarns = await self._repository.search(query.query_text, query.limit)

        dtos = tuple(
            YarnDto(
                id=yarn.id,
                name=yarn.name,
                brand_id=yarn.brand_id,
                weight=yarn.weight,
                fiber_types=tuple(yarn.fiber_types),
                gauge=yarn.gauge,
                care_instructions=yarn.care_instructions,
                description=yarn.description,
                needle_size=yarn.needle_size,
                ball_spec=yarn.ball_spec,
                crochet_hook_size_mm=yarn.crochet_hook_size_mm,
                tags=tuple(yarn.tags),
                colors=tuple(yarn.colors),
                balls_per_garment=tuple(yarn.balls_per_garment),
            )
            for yarn in yarns
        )

        message = (
            f"Found {len(dtos)} yarn{'s' if len(dtos) != 1 else ''} matching your query."
            if dtos
            else "No yarns found matching your query. Try different keywords."
        )

        return GetYarnRecommendationsResponse(results=dtos, total=len(dtos), message=message)
