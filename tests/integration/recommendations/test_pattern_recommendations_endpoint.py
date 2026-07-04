from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from yarn_plugin.main import app
from yarn_plugin.recommendations.domain.model.difficulty import Difficulty
from yarn_plugin.recommendations.domain.model.language import Language
from yarn_plugin.recommendations.domain.model.needle_size import NeedleSize
from yarn_plugin.recommendations.domain.model.pattern import Pattern
from yarn_plugin.recommendations.domain.model.pattern_category import PatternCategory
from yarn_plugin.recommendations.domain.model.yarn_weight import YarnWeight


@pytest.fixture()
def client() -> TestClient:
    return TestClient(app)


def make_pattern() -> Pattern:
    return Pattern(
        id=uuid4(),
        brand_id=uuid4(),
        name="Cozy Winter Sweater",
        difficulty=Difficulty.BEGINNER,
        yarn_weight=YarnWeight.WORSTED,
        category=PatternCategory.SWEATER,
        language=Language.ENGLISH,
        needle_size=NeedleSize(min_mm=4.0, max_mm=5.0),
        popularity_rating=4.5,
        tags=["cozy", "winter"],
    )


def test_pattern_recommendations_returns_results(client: TestClient) -> None:
    pattern = make_pattern()
    with patch(
        "yarn_plugin.recommendations.user_interface.http.get_pattern_recommendations_controller.SqlAlchemyPatternRepository"
    ) as mock_repo_class:
        mock_repo = AsyncMock()
        mock_repo.search.return_value = [pattern]
        mock_repo_class.return_value = mock_repo

        response = client.get("/recommendations/patterns?query=cozy+sweater")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["results"][0]["name"] == "Cozy Winter Sweater"
    assert "Found 1 pattern" in data["message"]


def test_pattern_recommendations_empty_results(client: TestClient) -> None:
    with patch(
        "yarn_plugin.recommendations.user_interface.http.get_pattern_recommendations_controller.SqlAlchemyPatternRepository"
    ) as mock_repo_class:
        mock_repo = AsyncMock()
        mock_repo.search.return_value = []
        mock_repo_class.return_value = mock_repo

        response = client.get("/recommendations/patterns?query=lace+shawl")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert data["results"] == []
    assert "No patterns found" in data["message"]


def test_pattern_recommendations_requires_query(client: TestClient) -> None:
    response = client.get("/recommendations/patterns")
    assert response.status_code == 422
