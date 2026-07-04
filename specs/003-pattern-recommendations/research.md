# Research: Pattern & Stitch Recommendations

## Decisions

### 1. Ravelry com a font de patrons, en viu (sense emmagatzematge propi)

**Decision**: `PatternRepositoryInterface` implementat per un adapter HTTP (`ravelry_pattern_repository.py`) que consulta l'API pública de Ravelry a cada petició. No es persisteix cap patró a la nostra base de dades.

**Rationale**: Evita el problema de drets d'autor (els patrons són disseny amb copyright) sense sacrificar dades reals — decisió presa amb la dev abans d'escriure l'spec. Ravelry és l'índex de patrons de knit/crochet més gran i establert.

**Alternatives considerades**:
- Catàleg propi curat (com Yarn/Brand) → descartada, requeriria crear contingut original o assumir risc legal de copiar patrons de tercers
- Altres índexs de patrons (LoveCrafts, etc.) → no descartats definitivament, però Ravelry és el punt de partida per volum i maduresa de l'API

---

### 2. Tests de l'adapter Ravelry amb fixtures gravades, no l'API real

**Decision**: Els tests d'integració de `ravelry_pattern_repository.py` fan servir respostes HTTP gravades (fixtures), no criden l'API de Ravelry real.

**Rationale**: L'API de Ravelry és una dependència externa fora del nostre control (rate limits, disponibilitat, canvis de contracte). Fer-la servir en CI faria la suite inestable i dependent de credencials/quota de tercers. Les fixtures gravades permeten validar el mapeig de resposta → domini de manera determinista, mantenint el 90% de cobertura exigit pel principi Test-First sense trencar-lo.

**Alternatives considerades**:
- Cridar l'API real en tests → descartada (flaky, depèn de credencials i quota externa)
- Mockear a nivell de `httpx` sense fixtures reals → possible complement, però les fixtures gravades capturen millor el contracte real de resposta de Ravelry

---

### 3. Technique com a catàleg propi (mateix patró que Yarn/Brand)

**Decision**: `Technique` es guarda a PostgreSQL via SQLAlchemy, seguint exactament el mateix patró d'ORM/repositori que `Yarn`/`Brand` — no hi ha res extern a consultar per a les tècniques.

**Rationale**: A diferència dels patrons, les instruccions de com fer un punt no tenen problema de copyright (són tècniques genèriques, no dissenys), i el catàleg és petit (~20-50 entrades), fàcil de curar manualment. Reutilitzar el patró existent (ORM + repository interface + SQLAlchemy adapter) manté consistència arquitectònica sense inventar res nou.

**Alternatives considerades**:
- Consultar també una font externa (p.ex. una wiki de tècniques) → descartada per ara, sense una font fiable i estructurada equivalent a Ravelry per a tècniques
- Contingut estàtic en fitxers (YAML/JSON) en lloc de BD → descartada, trenca la consistència amb la resta del domini i complica la cerca per craft type

---

### 4. CraftType com a enum senzill, no una entitat separada

**Decision**: `CraftType` és un `StrEnum` (`KNIT`, `CROCHET`), igual que `YarnWeight` o `Difficulty` — no una taula/entitat pròpia.

**Rationale**: Només dos valors fixos i estables, sense atributs propis ni necessitat de gestió dinàmica. Un enum és la solució més simple que compleix el requisit (FR-007: distingir tècniques/patrons per ofici).

**Alternatives considerades**:
- Taula `craft_types` amb metadades pròpies → descartada, sobreenginyeria per a dos valors fixos (YAGNI, ja establert al constitution)
