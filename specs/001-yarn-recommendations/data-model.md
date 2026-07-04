# Data Model: Yarn & Pattern Recommendations

## Entities

### Brand
Representa una marca de llana o un dissenyador de patrons.

| Camp | Tipus | Restriccions |
|---|---|---|
| id | UUID | PK, auto-generat |
| name | string | NOT NULL, únic |
| website | string | nullable |
| description | string | nullable |
| created_at | timestamp | NOT NULL |

---

### Yarn
Representa un tipus de llana concret d'una marca.

| Camp | Tipus | Restriccions |
|---|---|---|
| id | UUID | PK, auto-generat |
| brand_id | UUID | FK → Brand |
| name | string | NOT NULL |
| weight | enum | NOT NULL: lace, fingering, sport, dk, worsted, aran, bulky, super_bulky |
| fiber_content | string | NOT NULL (ex: "100% merino", "80% wool 20% nylon") |
| description | string | nullable |
| tags | string[] | ex: ["beginner-friendly", "washable", "natural", "soft"] |
| search_vector | tsvector | actualitzat via trigger (name + description + tags) |
| created_at | timestamp | NOT NULL |

**Regles de validació**:
- `name` + `brand_id` han de ser únics (no duplicats)
- `weight` ha de ser un dels valors de l'enum
- `tags` pot ser buit però no null

---

### Pattern
Representa un patró de teixir d'un dissenyador.

| Camp | Tipus | Restriccions |
|---|---|---|
| id | UUID | PK, auto-generat |
| brand_id | UUID | FK → Brand (el dissenyador) |
| name | string | NOT NULL |
| difficulty | enum | NOT NULL: beginner, intermediate, advanced |
| yarn_weight | enum | NOT NULL — mateixos valors que Yarn.weight |
| category | enum | NOT NULL: sweater, hat, socks, shawl, blanket, accessory, other |
| language | enum | NOT NULL: ca, es, en (`Language`) |
| needle_min_mm / needle_max_mm | float | NOT NULL — rang d'agulles, reutilitza `NeedleSize` (mateix value object que Yarn) |
| recommended_yarn_id | UUID | FK → Yarn, nullable — llana concreta del catàleg que recomana el patró, si es coneix |
| popularity_rating | float | nullable, 1.0–5.0 — puntuació manual (no calculada) |
| description | string | nullable |
| tags | string[] | ex: ["cozy", "winter", "chunky", "colorwork"] |
| search_vector | tsvector | actualitzat via trigger |
| created_at | timestamp | NOT NULL |

**Regles de validació**:
- `name` + `brand_id` han de ser únics
- `difficulty`, `yarn_weight`, `category`, `language` han de ser valors de l'enum
- `popularity_rating`, si es proporciona, ha d'estar entre 1.0 i 5.0
- `needle_min_mm` ha de ser ≤ `needle_max_mm`

---

### Technique
Representa una tècnica/punt reutilitzable de knit o crochet, curada per nosaltres — independent de qualsevol patró.

| Camp | Tipus | Restriccions |
|---|---|---|
| id | UUID | PK, auto-generat |
| name | string | NOT NULL |
| craft_type | enum | NOT NULL: knit, crochet |
| instructions | string | NOT NULL — pas a pas, text pla |
| description | string | nullable |
| created_at | timestamp | NOT NULL |

**Regles de validació**:
- `name` + `craft_type` han de ser únics (el mateix nom pot existir en knit i crochet com a tècniques diferents)
- `instructions` no pot ser buit

### CraftType *(enum, no entitat)*
`knit` | `crochet` — usat per `Technique`. `Pattern` ja té el seu propi `yarn_weight`/`category` i no necessita `craft_type` per a aquesta versió (totes les patterns d'aquesta v1 són de teixir amb agulles; crochet a `Pattern` és una ampliació futura si cal).

## Relacions

```
Brand 1 ──── * Yarn
Brand 1 ──── * Pattern
Yarn   1 ──── * Pattern   (recommended_yarn_id, opcional)
```

`Technique` no té relació de BD amb `Pattern` en aquesta versió (v1) — és un catàleg independent consultable per separat. Creuar-los (saber quines tècniques necessita un patró) és una ampliació futura, no en l'abast d'aquest MVP.

## Notes d'implementació

- Els IDs són UUIDs generats a la capa d'aplicació (no a la BD) — consistent amb DDD (el domini controla la identitat).
- `search_vector` s'actualitza via trigger PostgreSQL per mantenir el domini lliure d'aquesta lògica d'infraestructura.
- Els `tags` es guarden com `text[]` a PostgreSQL — sense taula separada per a MVP.