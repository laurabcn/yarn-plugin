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
| description | string | nullable |
| tags | string[] | ex: ["cozy", "winter", "chunky", "colorwork"] |
| search_vector | tsvector | actualitzat via trigger |
| created_at | timestamp | NOT NULL |

**Regles de validació**:
- `name` + `brand_id` han de ser únics
- `difficulty`, `yarn_weight`, `category` han de ser valors de l'enum

---

## Relacions

```
Brand 1 ──── * Yarn
Brand 1 ──── * Pattern
```

## Notes d'implementació

- Els IDs són UUIDs generats a la capa d'aplicació (no a la BD) — consistent amb DDD (el domini controla la identitat).
- `search_vector` s'actualitza via trigger PostgreSQL per mantenir el domini lliure d'aquesta lògica d'infraestructura.
- Els `tags` es guarden com `text[]` a PostgreSQL — sense taula separada per a MVP.