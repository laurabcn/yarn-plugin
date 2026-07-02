# Implementation Plan: Yarn & Pattern Recommendations

**Branch**: `001-yarn-recommendations` | **Date**: 2026-07-02 | **Spec**: [spec.md](spec.md)

## Summary

Build a REST API that accepts natural language queries and returns ranked yarn and pattern recommendations. The API exposes an OpenAPI spec compatible with MCP (Claude) and GPT Actions. Architecture follows DDD + Hexagonal + CQRS, same pattern as kitt-api (PHP/Symfony).

## Technical Context

**Language/Version**: Python 3.12

**Primary Dependencies**: FastAPI 0.115, SQLAlchemy 2.0 (async), Alembic, asyncpg, Pydantic 2.8, mcp 1.0

**Storage**: PostgreSQL 16 — yarns, patterns, brands

**Testing**: pytest + pytest-asyncio + pytest-cov (90% min)

**Target Platform**: Linux server (Docker)

**Project Type**: Web service (REST API + MCP server)

**Performance Goals**: Queries return results in under 2 seconds (SC-001)

**Constraints**: No external AI calls for search in v1 — keyword + tag matching only. Semantic search is a future enhancement.

**Scale/Scope**: MVP — small catalogue (20–200 yarns/patterns), single server

## Constitution Check

| Principle | Status | Notes |
|---|---|---|
| I. API-First | ✅ | FastAPI auto-generates OpenAPI spec |
| II. Domain-First | ✅ | Domain layer has no FastAPI/SQLAlchemy imports |
| III. Respostes honestes | ✅ | Empty results return message, no hallucination possible |
| IV. Test-First | ✅ | pytest, 90% coverage enforced |
| V. DDD + Hexagonal + CQRS | ✅ | Query/Command handlers, repository interfaces in domain |

No violations. Proceeding to Phase 0.

## Project Structure

### Documentation (this feature)

```text
specs/001-yarn-recommendations/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── openapi-recommendations.yaml
└── tasks.md             # creat per /speckit-tasks
```

### Source Code

```text
src/yarn_plugin/
├── recommendations/
│   ├── domain/
│   │   ├── model/
│   │   │   ├── yarn.py          # Yarn aggregate
│   │   │   ├── pattern.py       # Pattern aggregate
│   │   │   └── brand.py         # Brand entity
│   │   ├── repository/
│   │   │   ├── yarn_repository_interface.py
│   │   │   └── pattern_repository_interface.py
│   │   └── service/
│   │       └── recommendation_scorer.py
│   ├── application/
│   │   ├── query/
│   │   │   ├── get_yarn_recommendations/
│   │   │   │   ├── query.py
│   │   │   │   ├── handler.py
│   │   │   │   └── response.py
│   │   │   └── get_pattern_recommendations/
│   │   │       ├── query.py
│   │   │       ├── handler.py
│   │   │       └── response.py
│   │   └── command/
│   │       └── register_yarn/
│   │           ├── command.py
│   │           └── handler.py
│   └── infrastructure/
│       └── repository/
│           ├── sqlalchemy_yarn_repository.py
│           └── sqlalchemy_pattern_repository.py
├── shared/
│   └── domain/
│       └── object/
│           └── non_empty_string.py
└── main.py

tests/
├── unit/
│   └── recommendations/
│       ├── domain/
│       └── application/
└── integration/
    └── recommendations/
        └── infrastructure/
```