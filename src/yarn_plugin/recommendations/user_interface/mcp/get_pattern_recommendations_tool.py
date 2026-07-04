from yarn_plugin.infrastructure.database import async_session_factory
from yarn_plugin.recommendations.application.query.get_pattern_recommendations.handler import (
    GetPatternRecommendationsHandler,
)
from yarn_plugin.recommendations.application.query.get_pattern_recommendations.query import (
    GetPatternRecommendationsQuery,
)
from yarn_plugin.recommendations.infrastructure.repository.sqlalchemy_pattern_repository import (
    SqlAlchemyPatternRepository,
)
from yarn_plugin.recommendations.user_interface.http.get_pattern_recommendations_controller import (
    PatternRecommendationsResponseModel,
    pattern_dto_to_response_model,
)


async def get_pattern_recommendations(query: str, limit: int = 5) -> PatternRecommendationsResponseModel:
    """Get real knitting/crochet pattern recommendations for a natural language query, e.g. "cozy
    beginner sweater pattern" or "colorwork hat for winter". Only returns patterns that actually exist
    in the catalog — never invents a pattern, designer, or specification. If nothing matches, says so
    plainly. Each pattern lists which yarn weight/needle size it needs and, if known, a specific
    recommended yarn from the catalog (cross-reference with get_yarn_recommendations).
    """
    async with async_session_factory() as session:
        repository = SqlAlchemyPatternRepository(session)
        handler = GetPatternRecommendationsHandler(repository)
        response = await handler.handle(GetPatternRecommendationsQuery(query_text=query, limit=limit))

        return PatternRecommendationsResponseModel(
            results=[pattern_dto_to_response_model(dto) for dto in response.results],
            total=response.total,
            message=response.message,
        )
