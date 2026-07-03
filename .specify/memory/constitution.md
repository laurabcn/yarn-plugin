<!-- Sync Impact Report
Version change: 1.1.0 → 1.2.0
Modified principles: II. Domain-First (added repository/exception conventions), IV. Test-First (added "feature ships complete" rule)
Added sections: none (existing principles expanded, no new principle added)
Templates requiring updates: ✅ plan-template.md (no changes needed — no new mandatory sections/constraints) / ✅ spec-template.md (no changes needed) / ✅ tasks-template.md (no changes needed)
-->

<!-- Previous Sync Impact Report (1.0.0)
Version change: 0.0.0 (template) → 1.0.0 (initial ratification)
Added sections: Core Principles, Tech Stack, Quality Gates, Governance
Templates requiring updates: ✅ constitution written from template
-->

# Yarn Plugin Constitution

## Core Principles

### I. API-First
Every capability MUST be exposed as a documented REST endpoint before any integration (MCP, GPT Actions) is added.
The OpenAPI spec is the source of truth — generated automatically by FastAPI, never written by hand.
Integrations (MCP, GPT Actions) are adapters over the API, not replacements.

### II. Domain-First
The domain layer MUST be free of framework and infrastructure dependencies.
All business logic (recommendation logic, scoring, search) lives in `domain/`.
Application and Infrastructure layers depend on Domain — never the reverse.
Enforced by import-linter architecture tests.

Repository methods return domain objects as-is; they never encode a business selection criterion
("the highlighted one", "the active one") — that decision belongs to a domain service, not the
repository. A repository/finder needing data for multiple entities MUST expose a batch method
(e.g. `find_by_ids`) — looping single lookups (N+1) is a defect, not a style preference.

Domain exceptions are specific, named classes — never a bare `ValueError`/`Exception` raised from
application or infrastructure code that a controller needs to distinguish. When wrapping a
lower-level failure, the cause MUST be chained with `raise NewException(...) from e` — never
silently dropped.

### III. Defensive and Transparent Responses
Every response MUST be honest about confidence and data completeness.
If the system doesn't have enough data to recommend, it MUST say so — never hallucinate or invent recommendations.
All recommendations MUST include the source of the data (brand info, pattern metadata, etc.).

### IV. Test-First (NON-NEGOTIABLE)
Tests are written before implementation. Red → Green → Refactor.
Minimum 90% coverage enforced by pytest-cov on every CI run.
Unit tests for domain and application. Integration tests for DB.

A feature ships complete in a single change: implementation, its test, and any new domain exception
it raises. The test is never a follow-up change — a handler without its test is a partial feature,
not a reviewable one.

### V. Arquitectura — DDD + Hexagonal + CQRS (+ Event Sourcing si cal)
L'arquitectura segueix DDD amb Hexagonal Architecture i CQRS, igual que kitt-api (PHP/Symfony) de THN.
- **DDD**: Domain, Application, Infrastructure, UI layers. El domini no depèn de res extern.
- **Hexagonal**: els ports (interfaces) al domini, els adapters (implementacions) a la infraestructura.
- **CQRS**: Commands (escriptura) i Queries (lectura) separats amb handlers propis.
- **Event Sourcing**: s'afegeix només quan hi hagi necessitat real d'auditoria o reconstrucció d'estat — no per defecte.

Simplicitat dins d'aquest marc: no afegir capes ni abstraccions fins que el cas d'ús ho requereixi. YAGNI.

## Tech Stack

- **Backend**: Python 3.12 + FastAPI (auto-generates OpenAPI spec)
- **Base de dades**: PostgreSQL 16 (SQLAlchemy async + Alembic migrations)
- **Contenidors**: Docker Compose
- **Primera integració IA**: MCP (Model Context Protocol) per a Claude
- **Frontend**: generat amb v0.dev quan calgui — fora d'aquest repo

## Quality Gates

Tots els punts MUST passar abans de fer merge a `main`:

- `make lint` — ruff
- `make typecheck` — mypy strict
- `make arch-check` — import-linter
- `make test` — pytest 90% cobertura mínima

Conventional Commits obligatori: `feat`, `fix`, `chore`, `test`, `docs`, `refactor`.

## Governance

Aquesta constitució té prioritat sobre qualsevol altra pràctica.
Els canvis requereixen descripció, raonament i actualització d'aquest fitxer.
La branca `main` és sempre desplegable.

**Version**: 1.2.0 | **Ratified**: 2026-07-02 | **Last Amended**: 2026-07-03