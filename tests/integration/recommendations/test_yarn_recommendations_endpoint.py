from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from yarn_plugin.main import app
from yarn_plugin.recommendations.domain.model.yarn import Yarn
from yarn_plugin.recommendations.domain.model.yarn_weight import YarnWeight


@pytest.fixture()
def client() -> TestClient:
    return TestClient(app)


def make_yarn() -> Yarn:
    return Yarn(
        id=uuid4(),
        brand_id=uuid4(),
        name="Drops Alaska",
        weight=YarnWeight.WORSTED,
        fiber_content="100% wool",
        tags=["beginner-friendly", "natural"],
    )


def test_health_check(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_yarn_recommendations_returns_results(client: TestClient) -> None:
    yarn = make_yarn()
    with patch(
        "yarn_plugin.recommendations.user_interface.http.get_yarn_recommendations_controller.SqlAlchemyYarnRepository"
    ) as mock_repo_class:
        mock_repo = AsyncMock()
        mock_repo.search.return_value = [yarn]
        mock_repo_class.return_value = mock_repo

        response = client.get("/recommendations/yarn?query=beginner+yarn")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["results"][0]["name"] == "Drops Alaska"
    assert "Found 1 yarn" in data["message"]


def test_yarn_recommendations_empty_results(client: TestClient) -> None:
    with patch(
        "yarn_plugin.recommendations.user_interface.http.get_yarn_recommendations_controller.SqlAlchemyYarnRepository"
    ) as mock_repo_class:
        mock_repo = AsyncMock()
        mock_repo.search.return_value = []
        mock_repo_class.return_value = mock_repo

        response = client.get("/recommendations/yarn?query=silk+lace")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert data["results"] == []
    assert "No yarns found" in data["message"]


def test_yarn_recommendations_requires_query(client: TestClient) -> None:
    response = client.get("/recommendations/yarn")
    assert response.status_code == 422
