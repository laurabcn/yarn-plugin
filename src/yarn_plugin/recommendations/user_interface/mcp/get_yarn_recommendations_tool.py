from yarn_plugin.infrastructure.database import async_session_factory
from yarn_plugin.recommendations.application.query.get_yarn_recommendations.handler import (
    GetYarnRecommendationsHandler,
)
from yarn_plugin.recommendations.application.query.get_yarn_recommendations.query import GetYarnRecommendationsQuery
from yarn_plugin.recommendations.infrastructure.repository.sqlalchemy_yarn_repository import SqlAlchemyYarnRepository
from yarn_plugin.recommendations.user_interface.http.get_yarn_recommendations_controller import (
    YarnRecommendationsResponseModel,
    yarn_dto_to_response_model,
)


async def get_yarn_recommendations(query: str, limit: int = 5) -> YarnRecommendationsResponseModel:
    """Get real yarn recommendations for a natural language query, e.g. "best yarn for a beginner
    knitting a sweater" or "soft cotton yarn for summer". Only returns yarns that actually exist in
    the catalog — never invents a yarn, brand, or specification. If nothing matches, says so plainly.
    """
    async with async_session_factory() as session:
        repository = SqlAlchemyYarnRepository(session)
        handler = GetYarnRecommendationsHandler(repository)
        response = await handler.handle(GetYarnRecommendationsQuery(query_text=query, limit=limit))

        return YarnRecommendationsResponseModel(
            results=[yarn_dto_to_response_model(dto) for dto in response.results],
            total=response.total,
            message=response.message,
        )
