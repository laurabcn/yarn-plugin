# Tasks: Yarn & Pattern Recommendations

**Feature**: 001-yarn-recommendations | **Date**: 2026-07-02
**Spec**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md)

---

## Phase 1 — Setup

- [ ] T001 Create full directory structure per plan.md under `src/yarn_plugin/`
- [ ] T002 Create `src/yarn_plugin/__init__.py` and all `__init__.py` files in subdirectories
- [ ] T003 Configure Alembic in `alembic.ini` and `alembic/env.py` pointing to PostgreSQL
- [ ] T004 Configure SQLAlchemy async engine in `src/yarn_plugin/infrastructure/database.py`

---

## Phase 2 — Foundational (blocking per a totes les user stories)

- [ ] T005 [P] Create `NonEmptyStringValue` value object in `src/yarn_plugin/shared/domain/object/non_empty_string.py`
- [ ] T006 [P] Create `YarnWeight` enum in `src/yarn_plugin/recommendations/domain/model/yarn_weight.py` with values: lace, fingering, sport, dk, worsted, aran, bulky, super_bulky
- [ ] T007 [P] Create `Difficulty` enum in `src/yarn_plugin/recommendations/domain/model/difficulty.py` with values: beginner, intermediate, advanced
- [ ] T008 [P] Create `PatternCategory` enum in `src/yarn_plugin/recommendations/domain/model/pattern_category.py` with values: sweater, hat, socks, shawl, blanket, accessory, other
- [ ] T009 Create `Brand` entity in `src/yarn_plugin/recommendations/domain/model/brand.py` with fields: id (UUID), name, website (nullable), description (nullable), created_at
- [ ] T010 Create SQLAlchemy `BrandModel` ORM table in `src/yarn_plugin/recommendations/infrastructure/repository/orm/brand_orm.py`
- [ ] T011 Create Alembic migration for `brands` table with `make migrate-create m="create_brands_table"`

---

## Phase 3 — US1: Yarn Recommendation by Natural Language Query

**Story goal**: `GET /recommendations/yarn?query=...` retorna llanes rellevants o llista buida honesta.

**Independent test**: `curl "http://localhost:8000/recommendations/yarn?query=best+yarn+for+beginners"` retorna JSON vàlid.

- [ ] T012 [P] [US1] Create `Yarn` aggregate in `src/yarn_plugin/recommendations/domain/model/yarn.py` with fields: id (UUID), brand_id, name, weight (YarnWeight), fiber_content, description, tags (list[str]), created_at
- [ ] T013 [P] [US1] Create `YarnRepositoryInterface` port in `src/yarn_plugin/recommendations/domain/repository/yarn_repository_interface.py` with methods: `save(yarn)`, `search(query: str, limit: int) -> list[Yarn]`
- [ ] T014 [US1] Create SQLAlchemy `YarnModel` ORM table in `src/yarn_plugin/recommendations/infrastructure/repository/orm/yarn_orm.py` with `search_vector tsvector` column
- [ ] T015 [US1] Create Alembic migration for `yarns` table with tsvector column and trigger with `make migrate-create m="create_yarns_table"`
- [ ] T016 [US1] Create `SqlAlchemyYarnRepository` adapter in `src/yarn_plugin/recommendations/infrastructure/repository/sqlalchemy_yarn_repository.py` implementing `YarnRepositoryInterface` — `search()` uses PostgreSQL full-text search
- [ ] T017 [US1] Create `GetYarnRecommendationsQuery` in `src/yarn_plugin/recommendations/application/query/get_yarn_recommendations/query.py` with fields: `query_text: str`, `limit: int = 5`
- [ ] T018 [US1] Create `GetYarnRecommendationsResponse` in `src/yarn_plugin/recommendations/application/query/get_yarn_recommendations/response.py` with fields: `results: list[YarnDto]`, `total: int`, `message: str`
- [ ] T019 [US1] Create `GetYarnRecommendationsHandler` in `src/yarn_plugin/recommendations/application/query/get_yarn_recommendations/handler.py` — crida el repositori i construeix la resposta; retorna missatge clar si no hi ha resultats
- [ ] T020 [US1] Create `GET /recommendations/yarn` endpoint in `src/yarn_plugin/recommendations/user_interface/http/get_yarn_recommendations_controller.py` — delega al handler, retorna `YarnRecommendationsResponse` Pydantic model
- [ ] T021 [US1] Register endpoint in `src/yarn_plugin/main.py` amb el router de recommendations
- [ ] T022 [US1] Write unit tests for `GetYarnRecommendationsHandler` in `tests/unit/recommendations/application/query/test_get_yarn_recommendations_handler.py` — mock del repositori
- [ ] T023 [US1] Write integration test for `GET /recommendations/yarn` in `tests/integration/recommendations/test_yarn_recommendations_endpoint.py`

---

## Phase 4 — US2: Pattern Recommendation by Natural Language Query

**Story goal**: `GET /recommendations/patterns?query=...` retorna patrons rellevants.

**Independent test**: `curl "http://localhost:8000/recommendations/patterns?query=cozy+sweater"` retorna JSON vàlid.

- [ ] T024 [P] [US2] Create `Pattern` aggregate in `src/yarn_plugin/recommendations/domain/model/pattern.py` with fields: id (UUID), brand_id (designer), name, difficulty (Difficulty), yarn_weight (YarnWeight), category (PatternCategory), description, tags, created_at
- [ ] T025 [P] [US2] Create `PatternRepositoryInterface` in `src/yarn_plugin/recommendations/domain/repository/pattern_repository_interface.py` with methods: `save(pattern)`, `search(query: str, limit: int) -> list[Pattern]`
- [ ] T026 [US2] Create SQLAlchemy `PatternModel` ORM in `src/yarn_plugin/recommendations/infrastructure/repository/orm/pattern_orm.py` amb `search_vector tsvector`
- [ ] T027 [US2] Create Alembic migration for `patterns` table amb `make migrate-create m="create_patterns_table"`
- [ ] T028 [US2] Create `SqlAlchemyPatternRepository` in `src/yarn_plugin/recommendations/infrastructure/repository/sqlalchemy_pattern_repository.py`
- [ ] T029 [US2] Create `GetPatternRecommendationsQuery`, `Response` i `Handler` a `src/yarn_plugin/recommendations/application/query/get_pattern_recommendations/` — mateix patró que US1
- [ ] T030 [US2] Create `GET /recommendations/patterns` endpoint in `src/yarn_plugin/recommendations/user_interface/http/get_pattern_recommendations_controller.py`
- [ ] T031 [US2] Register endpoint in `src/yarn_plugin/main.py`
- [ ] T032 [US2] Write unit tests per al handler en `tests/unit/recommendations/application/query/test_get_pattern_recommendations_handler.py`
- [ ] T033 [US2] Write integration test en `tests/integration/recommendations/test_pattern_recommendations_endpoint.py`

---

## Phase 5 — US3: Brand/Yarn Registration (admin)

**Story goal**: `POST /admin/yarns` permet registrar una llana nova al catàleg.

**Independent test**: `POST /admin/yarns` amb payload vàlid retorna 201 i la llana apareix a `GET /recommendations/yarn`.

- [ ] T034 [US3] Create `RegisterYarnCommand` in `src/yarn_plugin/recommendations/application/command/register_yarn/command.py` amb fields: name, brand_name, weight, fiber_content, description, tags
- [ ] T035 [US3] Create `RegisterYarnHandler` in `src/yarn_plugin/recommendations/application/command/register_yarn/handler.py` — cerca o crea la Brand, crea el Yarn, crida el repositori; llança excepció si ja existeix
- [ ] T036 [US3] Create `POST /admin/yarns` endpoint in `src/yarn_plugin/recommendations/user_interface/http/register_yarn_controller.py` — retorna 201 o 409
- [ ] T037 [US3] Register endpoint en `src/yarn_plugin/main.py`
- [ ] T038 [US3] Write unit tests per al handler en `tests/unit/recommendations/application/command/test_register_yarn_handler.py`
- [ ] T039 [US3] Write integration test en `tests/integration/recommendations/test_register_yarn_endpoint.py`

---

## Phase 6 — Polish & Cross-Cutting

- [ ] T040 [P] Validate 90% test coverage with `make coverage` — fix gaps if any
- [ ] T041 [P] Run `make qa` (lint + typecheck + arch-check + tests) and fix all issues
- [ ] T042 Update `CLAUDE.md` to mark US1, US2, US3 as completed and document next step: MCP integration
- [ ] T043 Seed the database with 10+ real yarn examples via a script at `scripts/seed.py`

---

## Dependencies

```
Phase 1 (Setup)
    └── Phase 2 (Foundational: Brand, enums, DB)
            ├── Phase 3 (US1: Yarn recommendations)  ← MVP
            ├── Phase 4 (US2: Pattern recommendations)
            └── Phase 5 (US3: Registration)
                        └── Phase 6 (Polish)
```

US3 i US4 poden desenvolupar-se en paral·lel un cop Phase 2 és completa.

## MVP Scope

**Mínim viable**: Phase 1 + Phase 2 + Phase 3 (T001–T023)

Amb això, un assistent d'IA pot consultar `GET /recommendations/yarn` i retornar recomanacions reals. Tot el que ve després és incremental.

## Resum

| Phase | Tasques | User Story |
|---|---|---|
| 1 — Setup | T001–T004 | — |
| 2 — Foundational | T005–T011 | — |
| 3 — US1 Yarn Recs | T012–T023 | P1 |
| 4 — US2 Pattern Recs | T024–T033 | P2 |
| 5 — US3 Registration | T034–T039 | P3 |
| 6 — Polish | T040–T043 | — |
| **Total** | **43 tasques** | |
