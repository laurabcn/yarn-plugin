from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest

from yarn_plugin.recommendations.domain.model.care_instructions import CareInstructions
from yarn_plugin.recommendations.domain.model.fiber_type import FiberType
from yarn_plugin.recommendations.domain.model.gauge import Gauge
from yarn_plugin.recommendations.domain.model.yarn import Yarn
from yarn_plugin.recommendations.domain.model.yarn_weight import YarnWeight
from yarn_plugin.recommendations.user_interface.mcp.get_yarn_recommendations_tool import (
    get_yarn_recommendations,
)


def make_yarn() -> Yarn:
    return Yarn(
        brand_id=uuid4(),
        name="Drops Alaska",
        weight=YarnWeight.ARAN,
        fiber_types=[FiberType.WOOL],
        gauge=Gauge(stitches=16, rows=22),
        care_instructions=CareInstructions(
            machine_washable=True,
            wash_temperature_celsius=30,
            wash_program="wool",
            bleach_allowed=False,
            tumble_dry_allowed=False,
            dry_clean_allowed=False,
            dry_flat=True,
            max_iron_temperature_celsius=110,
        ),
        tags=["beginner-friendly"],
    )


@pytest.mark.asyncio
async def test_returns_yarn_recommendations() -> None:
    with patch(
        "yarn_plugin.recommendations.user_interface.mcp.get_yarn_recommendations_tool.SqlAlchemyYarnRepository"
    ) as mock_repo_class:
        mock_repo = AsyncMock()
        mock_repo.search.return_value = [make_yarn()]
        mock_repo_class.return_value = mock_repo

        response = await get_yarn_recommendations(query="beginner wool", limit=3)

    assert response.total == 1
    assert response.results[0].name == "Drops Alaska"
    assert "Found 1 yarn" in response.message
    mock_repo.search.assert_called_once_with("beginner wool", 3)


@pytest.mark.asyncio
async def test_returns_honest_message_when_no_match() -> None:
    with patch(
        "yarn_plugin.recommendations.user_interface.mcp.get_yarn_recommendations_tool.SqlAlchemyYarnRepository"
    ) as mock_repo_class:
        mock_repo = AsyncMock()
        mock_repo.search.return_value = []
        mock_repo_class.return_value = mock_repo

        response = await get_yarn_recommendations(query="silk lace")

    assert response.total == 0
    assert response.results == []
    assert "No yarns found" in response.message
