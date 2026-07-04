# Implementation Plan: Pattern & Stitch Recommendations

**Branch**: `003-pattern-recommendations` | **Date**: 2026-07-03 | **Spec**: [spec.md](spec.md)

## Summary

Add two read-only recommendation capabilities alongside the existing yarn one: pattern recommendations
sourced live from Ravelry's public API (no local storage of third-party pattern content, only relayed
metadata with attribution), and stitch/technique how-to instructions from our own curated catalog. Same
DDD + Hexagonal + CQRS shape as `001-yarn-recommendations` — the only structural novelty is that the
`Pattern` repository's adapter is an HTTP client to a third-party API instead of SQLAlchemy/Postgres.

## Technical Context

**Language/Version**: Python 3.12

**Primary Dependencies**: FastAPI, httpx (Ravelry HTTP client), SQLAlchemy 2.0 (async) + Alembic (Technique storage only), Pydantic 2.8, mcp 1.0

**Storage**: PostgreSQL 16 for `techniques` only. `Pattern` has no local storage — Ravelry's API is the system of record, queried on demand.

**Testing**: pytest + pytest-asyncio + pytest-cov (90% min). The Ravelry adapter is tested against recorded HTTP fixtures (not the live API) so the suite stays deterministic and doesn't depend on Ravelry's uptime or rate limits during CI.

**Target Platform**: Linux server (Docker)

**Project Type**: Web service (REST API + MCP server)

**Performance Goals**: Technique queries return in under 2s (local DB, same target as yarn). Pattern queries return in under 3s (SC-001/SC-002), allowing headroom for the external API round-trip.

**Constraints**: Ravelry API availability, rate limits, and terms of use are an external dependency outside our control — FR-008 requires surfacing outages honestly rather than retrying indefinitely or fabricating a result. No local caching of pattern results in v1 (per spec Assumptions); revisit if latency or rate limits become a problem.

**Scale/Scope**: MVP — technique catalog is small and hand-curated (~20-50 entries at launch); pattern "scope" is effectively Ravelry's whole catalog, filtered per-query.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|---|---|---|
| I. API-First | ✅ | FastAPI auto-generates OpenAPI spec for both new endpoints |
| II. Domain-First | ✅ | `PatternRepositoryInterface`/`TechniqueRepositoryInterface` live in domain; neither knows about httpx or SQLAlchemy |
| III. Defensive and Transparent Responses | ✅ | No-match and external-service-unavailable are both honest, explicit responses (FR-005, FR-008) — never fabricated |
| IV. Test-First (NON-NEGOTIABLE) | ✅ | Unit tests mock both repository interfaces; the Ravelry HTTP adapter gets an additional integration test against recorded fixtures instead of the live API, so 90% coverage doesn't require hitting a third party in CI |
| IV. (repository conventions, v1.2.0 amendment) | ✅ | Ravelry adapter returns pattern data as-is (no business selection logic in the repository); a batch-lookup concern doesn't apply here since Ravelry queries are already single-request per search |
| V. Arquitectura — DDD + Hexagonal + CQRS | ✅ | Query handlers + repository interfaces in domain, adapters in infrastructure — same shape as `get_yarn_recommendations` |

No violations. Proceeding to Phase 0.

## Project Structure

### Documentation (this feature)

```text
specs/003-pattern-recommendations/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── openapi-pattern-recommendations.yaml
└── tasks.md             # creat per /speckit-tasks
```

### Source Code

```text
src/yarn_plugin/recommendations/
├── domain/
│   ├── model/
│   │   ├── pattern.py                       # Pattern entity — external-sourced, not persisted
│   │   ├── craft_type.py                    # CraftType enum (knit/crochet)
│   │   ├── pattern_category.py              # already exists
│   │   ├── difficulty.py                    # already exists
│   │   └── technique.py                     # Technique entity — owned/curated
│   └── repository/
│       ├── pattern_repository_interface.py
│       └── technique_repository_interface.py
├── application/
│   └── query/
│       ├── get_pattern_recommendations/
│       │   ├── query.py
│       │   ├── handler.py
│       │   └── response.py
│       └── get_technique/
│           ├── query.py
│           ├── handler.py
│           └── response.py
├── infrastructure/
│   └── repository/
│       ├── ravelry_pattern_repository.py    # HTTP adapter — implements PatternRepositoryInterface
│       ├── sqlalchemy_technique_repository.py
│       └── orm/
│           └── technique_orm.py
└── user_interface/
    └── http/
        ├── get_pattern_recommendations_controller.py
        └── get_technique_controller.py

tests/
├── unit/
│   └── recommendations/
│       ├── domain/
│       └── application/
│           └── query/
│               ├── get_pattern_recommendations/
│               └── get_technique/
└── integration/
    └── recommendations/
        ├── test_pattern_recommendations_endpoint.py   # Ravelry adapter against recorded fixtures
        └── test_technique_endpoint.py                 # real Postgres, same pattern as yarn's repository tests
```

**Structure Decision**: Extends the existing `recommendations` bounded context (no new bounded context)
— `Pattern` and `Technique` sit alongside `Yarn` and `Brand` as new aggregates, each with its own
repository interface and one adapter. This keeps CQRS query handlers and the HTTP layer consistent with
`get_yarn_recommendations`, and lets the MCP server (future work) expose `get_pattern_recommendations`
and `get_technique` the same way it will expose `get_yarn_recommendations`.

## Complexity Tracking

*No Constitution Check violations — table intentionally omitted.*
