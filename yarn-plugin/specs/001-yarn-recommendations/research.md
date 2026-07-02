# Research: Yarn & Pattern Recommendations

## Decisions

### 1. Cerca per keyword i tags (no embeddings en v1)

**Decision**: Cerca basada en keywords i tags amb PostgreSQL full-text search (`tsvector`/`tsquery`) o ILIKE simple.

**Rationale**: Per a un catàleg petit (20–200 items), full-text search de PostgreSQL és suficient i evita dependències d'IA externes. Semantic search (pgvector + embeddings) s'afegirà quan hi hagi evidència de necessitat real.

**Alternatives considerades**:
- pgvector + embeddings → descartada per v1 (complexitat innecessària, catàleg petit)
- Elasticsearch → descartada (overhead d'infraestructura excessiu per a MVP)

---

### 2. MCP com a primera integració IA

**Decision**: Implementar MCP server sobre la mateixa API FastAPI.

**Rationale**: MCP és el protocol natiu de Claude i és un estàndard obert creixent (Cursor, Zed, etc.). La mateixa API REST serveix de base; MCP és un adapter per sobre.

**Alternatives considerades**:
- GPT Actions primer → descartada (la dev prefereix Claude; MCP és més modern)
- Les dues alhora → descartada (YAGNI, MVP primer)

---

### 3. CQRS sense bus de missatges en v1

**Decision**: CQRS amb handlers cridats directament (sense MessageBus) en v1.

**Rationale**: Per a un servei petit sense cues ni events distribuïts, un bus de missatges és sobreenginyeria. Els handlers s'injecten directament via FastAPI dependency injection. S'afegirà bus si apareix necessitat d'events distribuïts.

**Alternatives considerades**:
- Kafka/Celery → descartada (sense justificació en v1)
- In-memory bus → possible refactor futur si creix

---

### 4. PostgreSQL tsvector per a cerca

**Decision**: Columna `search_vector tsvector` a les taules `yarns` i `patterns`, actualitzada via trigger.

**Rationale**: Permet cerca full-text eficient sense dependències externes. Compatible amb les queries en anglès del MVP.

**Alternatives considerades**:
- ILIKE → massa lent per a catàlegs grans, sense ranking
- pgvector → v2 quan calgui cerca semàntica
