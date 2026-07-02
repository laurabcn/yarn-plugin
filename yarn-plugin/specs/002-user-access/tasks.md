# Tasks: User Access (Invite-Only)

**Feature**: 002-user-access | **Date**: 2026-07-02
**Spec**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md)

---

## Phase 1 — Setup

- [ ] T001 Add `python-jose[cryptography]` and `passlib[bcrypt]` to `pyproject.toml` dependencies
- [ ] T002 Add `ADMIN_SECRET`, `JWT_SECRET`, `JWT_EXPIRE_HOURS` and `BASE_URL` to `src/yarn_plugin/config.py` — `BASE_URL` s'usa per construir l'invite link complet
- [ ] T003 Create full `user_access/` directory structure under `src/yarn_plugin/` per plan.md
- [ ] T004 Create all `__init__.py` files in new directories

---

## Phase 2 — Foundational

- [ ] T005 [P] Create domain exceptions in `src/yarn_plugin/user_access/domain/exception/`: `invitation_not_found.py`, `invitation_expired.py`, `invitation_already_used.py`, `invalid_credentials.py`
- [ ] T006 [P] Create `JwtService` in `src/yarn_plugin/user_access/infrastructure/security/jwt_service.py` — `encode(user_id, email) -> str` i `decode(token) -> dict`
- [ ] T007 [P] Create `PasswordService` in `src/yarn_plugin/user_access/infrastructure/security/password_service.py` — `hash(password) -> str` i `verify(password, hash) -> bool`
- [ ] T008 Create `Invitation` entity in `src/yarn_plugin/user_access/domain/model/invitation.py` — fields: id (UUID), email, token, expires_at, accepted_at (nullable), created_at. Methods: `is_expired() -> bool`, `is_used() -> bool`, `accept() -> None`
- [ ] T009 Create `User` aggregate in `src/yarn_plugin/user_access/domain/model/user.py` — fields: id (UUID), email, password_hash, invitation_id, created_at
- [ ] T010 [P] Create `InvitationRepositoryInterface` in `src/yarn_plugin/user_access/domain/repository/invitation_repository_interface.py` — methods: `save(invitation)`, `find_by_token(token) -> Invitation | None`, `find_all() -> list[Invitation]`
- [ ] T011 [P] Create `UserRepositoryInterface` in `src/yarn_plugin/user_access/domain/repository/user_repository_interface.py` — methods: `save(user)`, `find_by_email(email) -> User | None`
- [ ] T012 Create ORM models: `InvitationModel` in `src/yarn_plugin/user_access/infrastructure/repository/orm/invitation_orm.py` i `UserModel` in `src/yarn_plugin/user_access/infrastructure/repository/orm/user_orm.py`
- [ ] T013 Create `SqlAlchemyInvitationRepository` in `src/yarn_plugin/user_access/infrastructure/repository/sqlalchemy_invitation_repository.py`
- [ ] T014 Create `SqlAlchemyUserRepository` in `src/yarn_plugin/user_access/infrastructure/repository/sqlalchemy_user_repository.py`
- [ ] T015 Create admin auth dependency in `src/yarn_plugin/shared/user_interface/http/admin_middleware.py` — verifica `X-Admin-Secret` header contra `settings.admin_secret`
- [ ] T016 Create JWT auth dependency in `src/yarn_plugin/shared/user_interface/http/auth_middleware.py` — extreu i valida Bearer token, retorna user_id i email

---

## Phase 3 — US1: Admin Creates Invitation

**Story goal**: `POST /admin/invitations` crea una invitació amb token únic i 7 dies de validesa.

**Independent test**: `curl -X POST /admin/invitations -H "X-Admin-Secret: ..."` retorna 201 amb token.

- [ ] T017 [US1] Create `CreateInvitationCommand` in `src/yarn_plugin/user_access/application/command/create_invitation/command.py` — fields: email
- [ ] T018 [US1] Create `CreateInvitationHandler` in `src/yarn_plugin/user_access/application/command/create_invitation/handler.py` — genera token amb `secrets.token_urlsafe(32)`, crea `Invitation`, crida el repositori; retorna també l'invite_url complet (`{BASE_URL}/accept?token={token}`)
- [ ] T019 [US1] Create `POST /admin/invitations` controller in `src/yarn_plugin/user_access/user_interface/http/create_invitation_controller.py` — protegit per `admin_middleware`; resposta inclou `invite_url` a més del token
- [ ] T019b [US1] Create `GET /auth/invitation/{token}` controller in `src/yarn_plugin/user_access/user_interface/http/validate_invitation_controller.py` — endpoint públic que valida si un token és vàlid (no expirat, no usat); retorna 200 amb l'email o 400/404 — permet al frontend mostrar el formulari de password
- [ ] T020 [US1] Create `GET /admin/invitations` controller in `src/yarn_plugin/user_access/user_interface/http/list_invitations_controller.py` — retorna llista amb status calculat (pending/accepted/expired) i invite_url per cada una
- [ ] T021 [US1] Register routers en `src/yarn_plugin/main.py`
- [ ] T022 [US1] Write unit tests for `CreateInvitationHandler` in `tests/unit/user_access/application/command/test_create_invitation_handler.py` — verifica que l'invite_url conté el token i el BASE_URL
- [ ] T023 [US1] Write integration tests for `POST /admin/invitations` and `GET /auth/invitation/{token}` in `tests/integration/user_access/test_create_invitation_endpoint.py`

---

## Phase 4 — US2: User Accepts Invitation and Creates Account

**Story goal**: `POST /auth/accept-invitation` valida el token i crea el compte.

**Independent test**: `POST /auth/accept-invitation` amb token vàlid i password retorna 201.

- [ ] T024 [US2] Create `AcceptInvitationCommand` in `src/yarn_plugin/user_access/application/command/accept_invitation/command.py` — fields: token, password
- [ ] T025 [US2] Create `AcceptInvitationHandler` in `src/yarn_plugin/user_access/application/command/accept_invitation/handler.py` — busca invitació per token, valida expiració i ús, hash del password via `PasswordService`, crea `User`, marca invitació com acceptada
- [ ] T026 [US2] Create `POST /auth/accept-invitation` controller in `src/yarn_plugin/user_access/user_interface/http/accept_invitation_controller.py` — retorna 201, 400 o 404 segons el cas
- [ ] T027 [US2] Register router en `src/yarn_plugin/main.py`
- [ ] T028 [US2] Write unit tests for `AcceptInvitationHandler` in `tests/unit/user_access/application/command/test_accept_invitation_handler.py` — cobreix: token vàlid, token expirat, token ja usat, password curt
- [ ] T029 [US2] Write integration tests in `tests/integration/user_access/test_accept_invitation_endpoint.py`

---

## Phase 5 — US3: User Logs In and Gets JWT

**Story goal**: `POST /auth/login` retorna JWT vàlid per a usuaris registrats.

**Independent test**: Login amb credencials correctes retorna JWT; endpoint protegit accepta el JWT.

- [ ] T030 [US3] Create `LoginQuery` in `src/yarn_plugin/user_access/application/query/login/query.py` — fields: email, password
- [ ] T031 [US3] Create `LoginResponse` in `src/yarn_plugin/user_access/application/query/login/response.py` — fields: access_token, token_type
- [ ] T032 [US3] Create `LoginHandler` in `src/yarn_plugin/user_access/application/query/login/handler.py` — busca usuari per email, verifica password via `PasswordService`, genera JWT via `JwtService`; llança `InvalidCredentials` si falla (sense revelar quin camp és incorrecte)
- [ ] T033 [US3] Create `POST /auth/login` controller in `src/yarn_plugin/user_access/user_interface/http/login_controller.py`
- [ ] T034 [US3] Register router en `src/yarn_plugin/main.py`
- [ ] T035 [US3] Protect `POST /admin/yarns` endpoint with `auth_middleware` (get_current_user dependency)
- [ ] T036 [US3] Write unit tests for `LoginHandler` in `tests/unit/user_access/application/query/test_login_handler.py` — cobreix: credencials correctes, email inexistent, password incorrecte
- [ ] T037 [US3] Write integration tests in `tests/integration/user_access/test_login_endpoint.py`

---

## Phase 6 — Alembic Migrations

- [ ] T038 Create Alembic migration for `invitations` table with `make migrate-create m="create_invitations_table"`
- [ ] T039 Create Alembic migration for `users` table with `make migrate-create m="create_users_table"`

---

## Phase 7 — Polish

- [ ] T040 [P] Run `make qa` — lint + typecheck + arch-check + tests i corregir tots els errors
- [ ] T041 [P] Verify 90% coverage with `make coverage`
- [ ] T042 Update `CLAUDE.md` marcant US1, US2, US3 de user-access com completades

---

## Dependencies

```
Phase 1 (Setup)
    └── Phase 2 (Foundational: entitats, repositoris, serveis de seguretat)
            ├── Phase 3 (US1: Create Invitation)   ← MVP
            ├── Phase 4 (US2: Accept Invitation)
            └── Phase 5 (US3: Login + JWT)
                        └── Phase 6 (Migrations)
                                    └── Phase 7 (Polish)
```

US2 i US3 poden desenvolupar-se en paral·lel un cop Phase 2 és completa.

## MVP Scope

**Mínim viable**: Phase 1 + Phase 2 + Phase 3 + Phase 4 + Phase 5 (T001–T037)

Les migracions (T038–T039) requereixen Docker engegat i es fan manualment.

## Resum

| Phase | Tasques | User Story |
|---|---|---|
| 1 — Setup | T001–T004 | — |
| 2 — Foundational | T005–T016 | — |
| 3 — US1 Create Invitation | T017–T023 | P1 |
| 4 — US2 Accept Invitation | T024–T029 | P2 |
| 5 — US3 Login + JWT | T030–T037 | P3 |
| 6 — Migrations | T038–T039 | — |
| 7 — Polish | T040–T042 | — |
| **Total** | **43 tasques** | |
