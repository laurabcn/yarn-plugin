# Data Model: Pattern & Stitch Recommendations

> **Supersedes** the `Pattern` entity sketched in `specs/001-yarn-recommendations/data-model.md`
> (a locally-stored table with `brand_id`, `search_vector`, etc.). That design was never
> implemented — no `Pattern` table, ORM model, or repository exists in code. This spec replaces
> it: `Pattern` is now sourced live from Ravelry, not persisted locally at all.

## Entities

### Pattern *(not persisted — shape of the domain object built from Ravelry's response)*

Representa un patró real de Ravelry, retornat en viu a cada consulta.

| Camp | Tipus | Restriccions |
|---|---|---|
| external_id | string | id del patró a Ravelry |
| name | string | NOT NULL |
| category | enum | `PatternCategory` (ja existent) — mapejat des de la categoria de Ravelry |
| difficulty | enum | `Difficulty` (ja existent) — mapejat des de la dificultat de Ravelry, si disponible |
| craft_type | enum | `CraftType`: knit \| crochet |
| description | string | nullable |
| source_url | string | NOT NULL — enllaç al patró original a Ravelry (atribució, FR-003) |
| required_technique_names | string[] | noms de tècniques segons Ravelry; es resolen contra el catàleg propi de `Technique` (poden no coincidir — vegeu Edge Cases a spec.md) |

**Regles de validació**:
- No hi ha `id` intern ni persistència — `external_id` + `source_url` són la referència a la font real
- Si Ravelry no proporciona `difficulty` o `required_technique_names`, el camp és `null`/buit, mai inventat (FR-003, Edge Cases)

---

### Technique
Representa una tècnica/punt reutilitzable de knit o crochet, curada per nosaltres.

| Camp | Tipus | Restriccions |
|---|---|---|
| id | UUID | PK, auto-generat |
| name | string | NOT NULL |
| craft_type | enum | NOT NULL: knit, crochet |
| instructions | string | NOT NULL — pas a pas, text pla |
| description | string | nullable |
| created_at | timestamp | NOT NULL |

**Regles de validació**:
- `name` + `craft_type` han de ser únics (el mateix nom pot existir en knit i crochet com a tècniques diferents — FR-007)
- `instructions` no pot ser buit

---

### CraftType *(enum, no entitat)*
`knit` | `crochet` — comparteix valors entre `Pattern` i `Technique`.

## Relacions

```
Pattern (extern, Ravelry) ····› Technique (propi, per nom + craft_type)
```

La relació entre `Pattern` i `Technique` és una referència feble per nom (`required_technique_names` ↔ `Technique.name` + `Technique.craft_type`), no una FK de base de dades — `Pattern` no viu a la nostra BD.

## Notes d'implementació

- `Technique` segueix exactament el mateix patró que `Yarn`/`Brand`: IDs UUID generats a la capa d'aplicació, repository interface al domini, adapter SQLAlchemy a infraestructura.
- `Pattern` no té ORM ni migració — el seu "repositori" (`RavelryPatternRepository`) implementa `PatternRepositoryInterface` cridant l'API HTTP de Ravelry i mapejant la resposta a l'objecte de domini `Pattern` directament, sense pas per BD.
- La resolució de `required_technique_names` contra el catàleg de `Technique` és responsabilitat del query handler (o d'un domain service dedicat si la lògica creix), no del repositori de patrons.
