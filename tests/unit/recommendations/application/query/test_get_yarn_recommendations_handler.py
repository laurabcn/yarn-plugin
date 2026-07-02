from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from yarn_plugin.recommendations.application.query.get_yarn_recommendations.handler import (
    GetYarnRecommendationsHandler,
)
from yarn_plugin.recommendations.application.query.get_yarn_recommendations.query import GetYarnRecommendationsQuery
from yarn_plugin.recommendations.domain.model.yarn import Yarn
from yarn_plugin.recommendations.domain.model.yarn_weight import YarnWeight


def make_yarn(name: str = "Test Yarn") -> Yarn:
    return Yarn(
        brand_id=uuid4(),
        name=name,
        weight=YarnWeight.WORSTED,
        fiber_content="100% wool",
        tags=["beginner-friendly"],
    )


@pytest.mark.asyncio
async def test_returns_yarns_when_found() -> None:
    repository = AsyncMock()
    repository.search.return_value = [make_yarn("Drops Alaska")]

    handler = GetYarnRecommendationsHandler(repository)
    response = await handler.handle(GetYarnRecommendationsQuery(query_text="beginner yarn"))

    assert response.total == 1
    assert response.results[0].name == "Drops Alaska"
    assert "Found 1 yarn" in response.message


@pytest.mark.asyncio
async def test_returns_empty_with_honest_message_when_no_results() -> None:
    repository = AsyncMock()
    repository.search.return_value = []

    handler = GetYarnRecommendationsHandler(repository)
    response = await handler.handle(GetYarnRecommendationsQuery(query_text="silk lace"))

    assert response.total == 0
    assert response.results == ()
    assert "No yarns found" in response.message


@pytest.mark.asyncio
async def test_respects_limit() -> None:
    repository = AsyncMock()
    repository.search.return_value = [make_yarn(f"Yarn {i}") for i in range(3)]

    handler = GetYarnRecommendationsHandler(repository)
    await handler.handle(GetYarnRecommendationsQuery(query_text="wool", limit=3))

    repository.search.assert_called_once_with("wool", 3)
