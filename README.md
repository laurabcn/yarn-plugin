# Yarn Plugin

API per a recomanacions de llanes i patrons de teixir, dissenyada per ser consumida per assistents d'IA.

## Què és

Yarn Plugin és una API REST que respon preguntes sobre llanes, patrons i tècniques de teixir. Qualsevol assistent d'IA (Claude, ChatGPT, Gemini...) pot consultar-la per donar respostes precises i actualitzades als seus usuaris.

**Exemples de preguntes que respon:**
- "What yarn do you recommend for a beginner knitting a sweater?"
- "Best knitting patterns for chunky yarn?"
- "What needle size for Drops Alaska yarn?"

## Integracions

| Plataforma | Protocol | Estat |
|---|---|---|
| Claude | MCP (Model Context Protocol) | Planificat |
| ChatGPT | GPT Actions | Futur |
| Gemini | Extensions | Futur |

L'API és genèrica — el mateix endpoint serveix per a totes les plataformes.

## Stack

- **Backend**: Python 3.12 + FastAPI
- **Base de dades**: PostgreSQL 16
- **Contenidors**: Docker Compose
- **Validació**: ruff + mypy + import-linter + pytest (90% cobertura mínima)

## Arquitectura

Segueix DDD + Arquitectura Hexagonal (mateix patró que kitt-api de THN):

```
src/yarn_plugin/
├── recommendations/      # bounded context principal
│   ├── domain/          # lògica de negoci pura
│   ├── application/     # casos d'ús (commands + queries)
│   └── infrastructure/  # repositoris, clients externs
└── shared/              # codi compartit
```

## Posada en marxa

```bash
git clone https://github.com/laurabcn/yarn-plugin.git
cd yarn-plugin
make setup
make start
```

L'API estarà disponible a `http://localhost:8000`.
Documentació OpenAPI: `http://localhost:8000/docs`

## Comandes

```bash
make setup        # Construir contenidors
make start        # Iniciar
make stop         # Aturar
make test         # Tests (90% cobertura mínima)
make qa           # Suite completa: lint + types + arch + tests
make migrate      # Executar migracions
```

## Relació amb yarn-visibility

[yarn-visibility](https://github.com/laurabcn/yarn-visibility) és un projecte complementari que monitoritxa com les IAs mencionen marques i patronistes. yarn-plugin és la peça que *alimenta* les IAs; yarn-visibility és la que *mesura* el resultat.
