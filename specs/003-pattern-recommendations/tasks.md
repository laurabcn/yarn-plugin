# Tasks: Pattern & Stitch Recommendations

**Feature**: 003-pattern-recommendations | **Date**: 2026-07-03
**Spec**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md)

---

## Phase 1 — Setup

- [ ] T001 Add `ravelry_api_key: str` and `ravelry_base_url: str = "https://api.ravelry.com"` fields to `Settings` in `src/yarn_plugin/config.py`
- [ ] T002 Document the required `RAVELRY_API_KEY` env var (README or `.env.example`) — `httpx` is already a project dependency, no new package needed

---

## Phase 2 — Foundational (blocking per a totes les user stories)

- [ ] T003 [P] Create `CraftType` enum in `src/yarn_plugin/recommendations/domain/model/craft_type.py` with values: knit, crochet

---

## Phase 3 — US1: Pattern Recommendation via Ravelry (P1)

**Story goal**: `GET /recommendations/patterns?query=...` retorna patrons reals consultats en viu a Ravelry, o un missatge honest si no n'hi ha o Ravelry no respon.

**Independent test**: `curl "http://localhost:8000/recommendations/patterns?query=cozy+beginner+sweater"` retorna JSON vàlid amb `source_url` d'atribució.

- [ ] T004 [P] [US1] Create `Pattern` domain object (no ORM, no persistència) in `src/yarn_plugin/recommendations/domain/model/pattern.py` with fields: external_id, name, category (PatternCategory), difficulty (Difficulty | None), craft_type (CraftType), description (str | None), source_url, required_technique_names (list[str])
- [ ] T005 [P] [US1] Create `PatternRepositoryInterface` port in `src/yarn_plugin/recommendations/domain/repository/pattern_repository_interface.py` with method: `search(query: str, limit: int) -> list[Pattern]`
- [ ] T006 [US1] Record Ravelry HTTP fixtures (sample real responses, credentials redacted) under `tests/fixtures/ravelry/` for use in adapter tests (per research.md #2)
- [ ] T007 [US1] Create `RavelryPatternRepository` adapter in `src/yarn_plugin/recommendations/infrastructure/repository/ravelry_pattern_repository.py` implementing `PatternRepositoryInterface` via `httpx` — maps Ravelry's response shape to `Pattern`, raises a specific exception (not a bare `ValueError`, per constitution v1.2.0) when Ravelry is unavailable/errors
- [ ] T008 [US1] Create `GetPatternRecommendationsQuery` in `src/yarn_plugin/recommendations/application/query/get_pattern_recommendations/query.py` with fields: `query_text: str`, `limit: int = 5`
- [ ] T009 [US1] Create `GetPatternRecommendationsResponse` in `src/yarn_plugin/recommendations/application/query/get_pattern_recommendations/response.py` with fields: `results: tuple[PatternDto, ...]`, `total: int`, `message: str`
- [ ] T010 [US1] Create `GetPatternRecommendationsHandler` in `src/yarn_plugin/recommendations/application/query/get_pattern_recommendations/handler.py` — calls the repository, catches the Ravelry-unavailable exception and returns an honest "temporarily unavailable" message instead of propagating a raw 500
- [ ] T011 [US1] Create `GET /recommendations/patterns` endpoint in `src/yarn_plugin/recommendations/user_interface/http/get_pattern_recommendations_controller.py` — maps the Ravelry-unavailable case to HTTP 503 (per [[handling-exceptions]])
- [ ] T012 [US1] Register endpoint in `src/yarn_plugin/main.py`
- [ ] T013 [P] [US1] Write unit tests for `GetPatternRecommendationsHandler` in `tests/unit/recommendations/application/query/test_get_pattern_recommendations_handler.py` — mock the repository; cover found / no-match / Ravelry-unavailable cases
- [ ] T014 [US1] Write integration test for the `RavelryPatternRepository` adapter in `tests/integration/recommendations/test_ravelry_pattern_repository.py` against the recorded fixtures from T006 (no live Ravelry calls)
- [ ] T015 [US1] Write integration test for `GET /recommendations/patterns` in `tests/integration/recommendations/test_pattern_recommendations_endpoint.py` (mocked repository, same pattern as the yarn endpoint test)

---

## Phase 4 — US2: Stitch/Technique How-To (P2)

**Story goal**: `GET /recommendations/techniques?query=...` retorna instruccions pas a pas d'una tècnica del catàleg propi.

**Independent test**: `curl "http://localhost:8000/recommendations/techniques?query=how+do+I+purl"` retorna JSON vàlid, sense dependre de cap dada de patrons.

- [ ] T016 [P] [US2] Create `Technique` aggregate in `src/yarn_plugin/recommendations/domain/model/technique.py` with fields: id (UUID), name, craft_type (CraftType), instructions, description (str | None), created_at
- [ ] T017 [P] [US2] Create `TechniqueRepositoryInterface` port in `src/yarn_plugin/recommendations/domain/repository/technique_repository_interface.py` with methods: `save(technique)`, `search(query: str, craft_type: CraftType | None, limit: int) -> list[Technique]`
- [ ] T018 [US2] Create SQLAlchemy `TechniqueModel` ORM in `src/yarn_plugin/recommendations/infrastructure/repository/orm/technique_orm.py`
- [ ] T019 [US2] Import `TechniqueModel` in `src/yarn_plugin/recommendations/infrastructure/repository/orm/__init__.py` so Alembic autogenerate picks it up (see the ORM-registration fix from the Yarn migration work)
- [ ] T020 [US2] Generate and apply the Alembic migration for the `techniques` table with `docker compose run --rm api alembic revision --autogenerate -m "create techniques table"`, then `make migrate`
- [ ] T021 [US2] Create `SqlAlchemyTechniqueRepository` adapter in `src/yarn_plugin/recommendations/infrastructure/repository/sqlalchemy_technique_repository.py`
- [ ] T022 [US2] Create `GetTechniqueQuery`, `Response` (with `TechniqueDto`) and `Handler` in `src/yarn_plugin/recommendations/application/query/get_technique/` — same shape as US1; handler never guesses a craft type when the name is ambiguous across knit/crochet (spec US2 acceptance scenario 2)
- [ ] T023 [US2] Create `RegisterTechniqueCommand` and `RegisterTechniqueCommandHandler` in `src/yarn_plugin/recommendations/application/command/register_technique/` — needed to seed the catalog (per [[command-handlers]])
- [ ] T024 [US2] Create `GET /recommendations/techniques` endpoint (with optional `craft_type` query param) in `src/yarn_plugin/recommendations/user_interface/http/get_technique_controller.py`
- [ ] T025 [US2] Create `POST /admin/techniques` endpoint in `src/yarn_plugin/recommendations/user_interface/http/register_technique_controller.py`
- [ ] T026 [US2] Register both endpoints in `src/yarn_plugin/main.py`
- [ ] T027 [P] [US2] Write unit tests for `GetTechniqueHandler` in `tests/unit/recommendations/application/query/test_get_technique_handler.py` — cover found / no-match / ambiguous-craft-type cases
- [ ] T028 [P] [US2] Write unit tests for `RegisterTechniqueCommandHandler` in `tests/unit/recommendations/application/command/test_register_technique_handler.py`
- [ ] T029 [US2] Write integration test for `GET /recommendations/techniques` and `POST /admin/techniques` in `tests/integration/recommendations/test_technique_endpoint.py`

---

## Phase 5 — US3: Cross-Reference Pattern Techniques (P3)

**Story goal**: Els noms de tècniques que reporta un patró de Ravelry es resolen contra el catàleg propi de `Technique`.

**Independent test**: Amb un patró que requereix "purl stitch" i "cast on", i "purl stitch" existent al catàleg propi però "cast on" no, la resposta marca quina referència no s'ha pogut resoldre.

**Depends on**: Phase 3 (US1) and Phase 4 (US2) both complete.

- [ ] T030 [US3] Extend `GetPatternRecommendationsHandler` (`src/yarn_plugin/recommendations/application/query/get_pattern_recommendations/handler.py`) to resolve each `Pattern.required_technique_names` entry against `TechniqueRepositoryInterface`, marking unresolved names rather than dropping them (per spec Edge Cases)
- [ ] T031 [US3] Update `PatternDto`/`GetPatternRecommendationsResponse` to expose which required techniques resolved vs. didn't
- [ ] T032 [US3] Write unit test covering the mixed resolved/unresolved case in `tests/unit/recommendations/application/query/test_get_pattern_recommendations_handler.py`

---

## Phase 6 — Polish & Cross-Cutting

- [ ] T033 [P] Validate 90% test coverage with `make coverage` — fix gaps if any
- [ ] T034 [P] Run `make qa` (lint + typecheck + arch-check + tests) and fix all issues — `make qa` must NOT require real Ravelry credentials (per research.md #2)
- [ ] T035 Update `CLAUDE.md` roadmap to mark pattern/technique recommendations as done and note MCP integration as the next step
- [ ] T036 Seed the technique catalog with 20-50 real knit/crochet techniques via `POST /admin/techniques` or a script at `scripts/seed_techniques.py`
- [ ] T037 Resolve the `001-yarn-recommendations` supersession noted in `003-pattern-recommendations/data-model.md`: mark Phase 4 (T024-T033) in `specs/001-yarn-recommendations/tasks.md` as superseded by this feature, per the pending decision with the user

---

## Dependencies

```
Phase 1 (Setup)
    └── Phase 2 (Foundational: CraftType)
            ├── Phase 3 (US1: Pattern recommendations via Ravelry)  ← MVP
            ├── Phase 4 (US2: Technique how-to)                    ← independent of US1
            └── Phase 5 (US3: Cross-reference)
                        └── requires BOTH Phase 3 and Phase 4 complete
                            └── Phase 6 (Polish)
```

US1 i US2 es poden desenvolupar en paral·lel un cop Phase 2 és completa — no comparteixen cap fitxer excepte `main.py` (registre de rutes) i el `CraftType` enum.

## MVP Scope

**Mínim viable**: Phase 1 + Phase 2 + Phase 3 (T001–T015)

Amb això, un assistent d'IA pot consultar `GET /recommendations/patterns` i obtenir patrons reals de Ravelry amb atribució. US2 (tècniques) i US3 (creuament) són incrementals i no bloquegen aquest MVP.

## Resum

| Phase | Tasques | User Story |
|---|---|---|
| 1 — Setup | T001–T002 | — |
| 2 — Foundational | T003 | — |
| 3 — US1 Pattern Recs (Ravelry) | T004–T015 | P1 |
| 4 — US2 Technique How-To | T016–T029 | P2 |
| 5 — US3 Cross-Reference | T030–T032 | P3 |
| 6 — Polish | T033–T037 | — |
| **Total** | **37 tasques** | |