# Implementation Plan: User Access (Invite-Only)

**Branch**: `002-user-access` | **Date**: 2026-07-02 | **Spec**: [spec.md](spec.md)

## Summary

Implement invite-only user registration and JWT authentication. Admin creates invitations via a static-secret-protected endpoint. Users accept invitations and create accounts. Registered users log in and receive JWT tokens to call protected endpoints. Architecture follows DDD + Hexagonal + CQRS, same bounded context pattern as kitt-api `UserAccess`.

## Technical Context

**Language/Version**: Python 3.12

**Primary Dependencies**:
- `python-jose[cryptography]` — JWT generation and validation
- `passlib[bcrypt]` — password hashing
- `fastapi.security` — HTTP Bearer token extraction

**Storage**: PostgreSQL 16 — `users` + `invitations` tables

**Testing**: pytest + pytest-asyncio (90% min)

**Target Platform**: Linux server (Docker)

**Project Type**: Web service — nou bounded context `user_access/` al costat de `recommendations/`

**Performance Goals**: Login sota 1 segon (SC-003)

**Constraints**: JWT stateless (sense revocació en v1). Admin auth via static `ADMIN_SECRET` env var.

## Constitution Check

| Principle | Status | Notes |
|---|---|---|
| I. API-First | ✅ | FastAPI auto-genera OpenAPI spec |
| II. Domain-First | ✅ | `User`, `Invitation` al domain, sense imports de FastAPI |
| III. Respostes honestes | ✅ | Login 401 no revela si l'email existeix |
| IV. Test-First | ✅ | pytest, 90% cobertura |
| V. DDD + Hexagonal + CQRS | ✅ | Commands per create-invitation i accept-invitation; Query per login |

Cap violació. Procedim a Phase 0.

## Project Structure

### Documentation (this feature)

```text
specs/002-user-access/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── openapi-user-access.yaml
└── tasks.md
```

### Source Code

```text
src/yarn_plugin/
└── user_access/
    ├── domain/
    │   ├── model/
    │   │   ├── user.py
    │   │   └── invitation.py
    │   ├── repository/
    │   │   ├── user_repository_interface.py
    │   │   └── invitation_repository_interface.py
    │   └── exception/
    │       ├── invitation_not_found.py
    │       ├── invitation_expired.py
    │       ├── invitation_already_used.py
    │       └── invalid_credentials.py
    ├── application/
    │   ├── command/
    │   │   ├── create_invitation/
    │   │   │   ├── command.py
    │   │   │   └── handler.py
    │   │   └── accept_invitation/
    │   │       ├── command.py
    │   │       └── handler.py
    │   └── query/
    │       └── login/
    │           ├── query.py
    │           ├── handler.py
    │           └── response.py
    ├── infrastructure/
    │   ├── repository/
    │   │   ├── orm/
    │   │   │   ├── user_orm.py
    │   │   │   └── invitation_orm.py
    │   │   ├── sqlalchemy_user_repository.py
    │   │   └── sqlalchemy_invitation_repository.py
    │   └── security/
    │       ├── jwt_service.py
    │       └── password_service.py
    └── user_interface/
        └── http/
            ├── create_invitation_controller.py
            ├── list_invitations_controller.py
            ├── accept_invitation_controller.py
            └── login_controller.py

src/yarn_plugin/shared/user_interface/http/
└── auth_middleware.py                    # get_current_user() FastAPI dependency

tests/
├── unit/user_access/
└── integration/user_access/
```
