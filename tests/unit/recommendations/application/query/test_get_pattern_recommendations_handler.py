from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from yarn_plugin.recommendations.application.query.get_pattern_recommendations.handler import (
    GetPatternRecommendationsHandler,
)
from yarn_plugin.recommendations.application.query.get_pattern_recommendations.query import (
    GetPatternRecommendationsQuery,
)
from yarn_plugin.recommendations.domain.model.difficulty import Difficulty
from yarn_plugin.recommendations.domain.model.language import Language
from yarn_plugin.recommendations.domain.model.needle_size import NeedleSize
from yarn_plugin.recommendations.domain.model.pattern import Pattern
from yarn_plugin.recommendations.domain.model.pattern_category import PatternCategory
from yarn_plugin.recommendations.domain.model.yarn_weight import YarnWeight


def make_pattern(name: str = "Test Pattern") -> Pattern:
    return Pattern(
        brand_id=uuid4(),
        name=name,
        difficulty=Difficulty.BEGINNER,
        yarn_weight=YarnWeight.WORSTED,
        category=PatternCategory.SWEATER,
        language=Language.ENGLISH,
        needle_size=NeedleSize(min_mm=4.0, max_mm=5.0),
        popularity_rating=4.5,
        tags=["cozy", "winter"],
    )


@pytest.mark.asyncio
async def test_returns_patterns_when_found() -> None:
    repository = AsyncMock()
    repository.search.return_value = [make_pattern("Cozy Sweater")]

    handler = GetPatternRecommendationsHandler(repository)
    response = await handler.handle(GetPatternRecommendationsQuery(query_text="cozy sweater"))

    assert response.total == 1
    assert response.results[0].name == "Cozy Sweater"
    assert "Found 1 pattern" in response.message


@pytest.mark.asyncio
async def test_returns_empty_with_honest_message_when_no_results() -> None:
    repository = AsyncMock()
    repository.search.return_value = []

    handler = GetPatternRecommendationsHandler(repository)
    response = await handler.handle(GetPatternRecommendationsQuery(query_text="lace shawl"))

    assert response.total == 0
    assert response.results == ()
    assert "No patterns found" in response.message


@pytest.mark.asyncio
async def test_respects_limit() -> None:
    repository = AsyncMock()
    repository.search.return_value = [make_pattern(f"Pattern {i}") for i in range(3)]

    handler = GetPatternRecommendationsHandler(repository)
    await handler.handle(GetPatternRecommendationsQuery(query_text="sweater", limit=3))

    repository.search.assert_called_once_with("sweater", 3)
