<!-- Sync Impact Report
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

### III. Defensive and Transparent Responses
Every response MUST be honest about confidence and data completeness.
If the system doesn't have enough data to recommend, it MUST say so — never hallucinate or invent recommendations.
All recommendations MUST include the source of the data (brand info, pattern metadata, etc.).

### IV. Test-First (NON-NEGOTIABLE)
Tests are written before implementation. Red → Green → Refactor.
Minimum 90% coverage enforced by pytest-cov on every CI run.
Unit tests for domain and application. Integration tests for DB.

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

**Version**: 1.1.0 | **Ratified**: 2026-07-02 | **Last Amended**: 2026-07-02