import uuid
from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from yarn_plugin.main import app
from yarn_plugin.user_access.application.command.create_invitation.handler import CreateInvitationResult
from yarn_plugin.user_access.domain.model.invitation import Invitation
from yarn_plugin.user_access.domain.model.user import User

CLIENT = TestClient(app)
ADMIN_HEADERS = {"X-Admin-Secret": "change-me-in-production"}


def _make_invitation(*, accepted_at: datetime | None = None, days_offset: int = 7) -> Invitation:
    now = datetime.now(timezone.utc)
    return Invitation(
        id=uuid.uuid4(),
        email="katia@example.com",
        token="test-token-abc",
        expires_at=now + timedelta(days=days_offset),
        created_at=now,
        accepted_at=accepted_at,
    )


# ── POST /admin/invitations ──────────────────────────────────────────────────

def test_create_invitation_returns_201() -> None:
    with patch(
        "yarn_plugin.user_access.user_interface.http.create_invitation_controller.SqlAlchemyInvitationRepository"
    ) as mock_cls:
        mock_repo = AsyncMock()
        mock_repo.save = AsyncMock()
        mock_cls.return_value = mock_repo

        response = CLIENT.post(
            "/admin/invitations",
            headers=ADMIN_HEADERS,
            json={"email": "katia@example.com"},
        )

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "katia@example.com"
    assert "invite_url" in data
    assert "token" in data["invite_url"]


def test_create_invitation_requires_admin_secret() -> None:
    response = CLIENT.post("/admin/invitations", json={"email": "katia@example.com"})
    assert response.status_code == 422


def test_create_invitation_wrong_secret_returns_401() -> None:
    response = CLIENT.post(
        "/admin/invitations",
        headers={"X-Admin-Secret": "wrong"},
        json={"email": "katia@example.com"},
    )
    assert response.status_code == 401


# ── GET /auth/invitation/{token} ─────────────────────────────────────────────

def test_validate_invitation_returns_200_for_valid_token() -> None:
    invitation = _make_invitation()
    with patch(
        "yarn_plugin.user_access.user_interface.http.validate_invitation_controller.SqlAlchemyInvitationRepository"
    ) as mock_cls:
        mock_repo = AsyncMock()
        mock_repo.find_by_token = AsyncMock(return_value=invitation)
        mock_cls.return_value = mock_repo

        response = CLIENT.get("/auth/invitation/test-token-abc")

    assert response.status_code == 200
    assert response.json()["email"] == "katia@example.com"


def test_validate_invitation_returns_404_for_unknown_token() -> None:
    with patch(
        "yarn_plugin.user_access.user_interface.http.validate_invitation_controller.SqlAlchemyInvitationRepository"
    ) as mock_cls:
        mock_repo = AsyncMock()
        mock_repo.find_by_token = AsyncMock(return_value=None)
        mock_cls.return_value = mock_repo

        response = CLIENT.get("/auth/invitation/unknown")

    assert response.status_code == 404


def test_validate_invitation_returns_400_for_expired_token() -> None:
    expired = _make_invitation(days_offset=-1)
    with patch(
        "yarn_plugin.user_access.user_interface.http.validate_invitation_controller.SqlAlchemyInvitationRepository"
    ) as mock_cls:
        mock_repo = AsyncMock()
        mock_repo.find_by_token = AsyncMock(return_value=expired)
        mock_cls.return_value = mock_repo

        response = CLIENT.get("/auth/invitation/expired-token")

    assert response.status_code == 400


# ── POST /auth/accept-invitation ─────────────────────────────────────────────

def test_accept_invitation_returns_201() -> None:
    invitation = _make_invitation()
    with (
        patch("yarn_plugin.user_access.user_interface.http.accept_invitation_controller.SqlAlchemyInvitationRepository") as inv_cls,
        patch("yarn_plugin.user_access.user_interface.http.accept_invitation_controller.SqlAlchemyUserRepository") as user_cls,
    ):
        inv_repo = AsyncMock()
        inv_repo.find_by_token = AsyncMock(return_value=invitation)
        inv_repo.save = AsyncMock()
        inv_cls.return_value = inv_repo

        user_repo = AsyncMock()
        user_repo.save = AsyncMock()
        user_cls.return_value = user_repo

        response = CLIENT.post(
            "/auth/accept-invitation",
            json={"token": "test-token-abc", "password": "securepass123"},
        )

    assert response.status_code == 201
    assert response.json()["email"] == "katia@example.com"


def test_accept_invitation_returns_404_for_unknown_token() -> None:
    with (
        patch("yarn_plugin.user_access.user_interface.http.accept_invitation_controller.SqlAlchemyInvitationRepository") as inv_cls,
        patch("yarn_plugin.user_access.user_interface.http.accept_invitation_controller.SqlAlchemyUserRepository") as user_cls,
    ):
        inv_repo = AsyncMock()
        inv_repo.find_by_token = AsyncMock(return_value=None)
        inv_cls.return_value = inv_repo
        user_cls.return_value = AsyncMock()

        response = CLIENT.post(
            "/auth/accept-invitation",
            json={"token": "bad", "password": "securepass123"},
        )

    assert response.status_code == 404


# ── POST /auth/login ──────────────────────────────────────────────────────────

def test_login_returns_401_for_unknown_user() -> None:
    with patch("yarn_plugin.user_access.user_interface.http.login_controller.SqlAlchemyUserRepository") as mock_cls:
        mock_repo = AsyncMock()
        mock_repo.find_by_email = AsyncMock(return_value=None)
        mock_cls.return_value = mock_repo

        response = CLIENT.post("/auth/login", json={"email": "nobody@example.com", "password": "pass"})

    assert response.status_code == 401