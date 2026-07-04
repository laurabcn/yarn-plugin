from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest

from yarn_plugin.recommendations.domain.model.difficulty import Difficulty
from yarn_plugin.recommendations.domain.model.language import Language
from yarn_plugin.recommendations.domain.model.needle_size import NeedleSize
from yarn_plugin.recommendations.domain.model.pattern import Pattern
from yarn_plugin.recommendations.domain.model.pattern_category import PatternCategory
from yarn_plugin.recommendations.domain.model.yarn_weight import YarnWeight
from yarn_plugin.recommendations.user_interface.mcp.get_pattern_recommendations_tool import (
    get_pattern_recommendations,
)


def make_pattern() -> Pattern:
    return Pattern(
        brand_id=uuid4(),
        name="Cozy Winter Sweater",
        difficulty=Difficulty.BEGINNER,
        yarn_weight=YarnWeight.WORSTED,
        category=PatternCategory.SWEATER,
        language=Language.ENGLISH,
        needle_size=NeedleSize(min_mm=4.0, max_mm=5.0),
        tags=["cozy", "winter"],
    )


@pytest.mark.asyncio
async def test_returns_pattern_recommendations() -> None:
    with patch(
        "yarn_plugin.recommendations.user_interface.mcp.get_pattern_recommendations_tool.SqlAlchemyPatternRepository"
    ) as mock_repo_class:
        mock_repo = AsyncMock()
        mock_repo.search.return_value = [make_pattern()]
        mock_repo_class.return_value = mock_repo

        response = await get_pattern_recommendations(query="cozy sweater", limit=3)

    assert response.total == 1
    assert response.results[0].name == "Cozy Winter Sweater"
    assert "Found 1 pattern" in response.message
    mock_repo.search.assert_called_once_with("cozy sweater", 3)


@pytest.mark.asyncio
async def test_returns_honest_message_when_no_match() -> None:
    with patch(
        "yarn_plugin.recommendations.user_interface.mcp.get_pattern_recommendations_tool.SqlAlchemyPatternRepository"
    ) as mock_repo_class:
        mock_repo = AsyncMock()
        mock_repo.search.return_value = []
        mock_repo_class.return_value = mock_repo

        response = await get_pattern_recommendations(query="lace shawl")

    assert response.total == 0
    assert response.results == []
    assert "No patterns found" in response.message
