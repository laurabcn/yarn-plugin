# CLAUDE.md — Yarn Plugin

Instruccions per a Claude Code en aquest repositori.

## Context del producte

Yarn Plugin és una API per a recomanacions de llanes i patrons de teixir, dissenyada per ser consumida per assistents d'IA via MCP (Claude) i GPT Actions (ChatGPT).

**La idea central:** quan algú pregunta a Claude "quina llana recomanes per a principiants?", Claude pot consultar aquesta API i retornar recomanacions reals i actualitzades en lloc d'inventar-les.

## Decisions preses (no reobrir)

- **Stack**: Python 3.12 + FastAPI + PostgreSQL + Docker. Sense Celery/Redis (l'API respon en síncron).
- **Primera integració**: MCP per a Claude, no GPT Actions.
- **Arquitectura**: DDD + Hexagonal, mateix patró que kitt-api (PHP/Symfony) de THN — la dev coneix aquest patró bé.
- **Sense frontend**: el frontend es generarà amb v0.dev quan calgui.

## Arquitectura

```
src/yarn_plugin/
├── recommendations/      # bounded context principal
│   ├── domain/
│   │   ├── model/       # Yarn, Pattern, Brand
│   │   └── service/     # lògica de cerca i scoring
│   ├── application/
│   │   └── query/       # GetYarnRecommendationsQuery, etc.
│   └── infrastructure/
│       └── repository/  # SQLAlchemy + PostgreSQL
└── shared/
    └── domain/
```

## Estat actual

- [x] Scaffold inicial: Docker, FastAPI, pyproject.toml, Makefile
- [x] `/health` endpoint
- [x] Models de domini (Yarn, Pattern, Brand)
- [x] Migracions Alembic
- [x] Endpoints de recomanació (`GET /recommendations/yarn`, `GET /recommendations/patterns`)
- [x] MCP server integration (`src/yarn_plugin/mcp_server.py` — `get_yarn_recommendations`, `get_pattern_recommendations`)
- [ ] OpenAPI spec completa

## Proper pas

- Provar el servidor MCP des de Claude Desktop/Code de debò (configurar-lo com a servidor stdio local)
- `Technique` (com fer un punt de knit/crochet) — spec ja escrita a `specs/001-yarn-recommendations` (Phase 7, US4)
- Considerar transport HTTP/remot per al servidor MCP quan calgui desplegar-lo fora de local

Seguir el flux de spec-kit: `/speckit-specify` → `/speckit-plan` → `/speckit-tasks` → `/speckit-implement`

## Convencions de codi

- Tots els fitxers amb `from __future__ import annotations` i type hints complets
- Mypy strict — cap `Any` sense justificació
- Ruff per a format i lint
- Import-linter per a regles d'arquitectura (Domain no pot importar Infrastructure)
- Conventional Commits: `feat`, `fix`, `chore`, `test`, `docs`, `refactor`
- 90% cobertura mínima de tests

## Comandes útils

```bash
make start        # Iniciar Docker
make test         # Tests
make qa           # Suite completa
make migrate      # Migracions
```

## Context de la dev

- 5 anys d'experiència a THN (The Hotels Network) amb PHP/Symfony i DDD
- Coneix bé kitt-api — usar-lo com a referència d'arquitectura quan calgui
- Aprenent Python i FastAPI — explicar les diferències respecte PHP quan sigui rellevant
- Objectiu: aprendre IA i millorar el CV per buscar feina