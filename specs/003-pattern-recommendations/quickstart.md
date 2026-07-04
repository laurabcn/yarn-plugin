# Quickstart & Validation Guide

## Prerequisites

```bash
git clone https://github.com/laurabcn/yarn-plugin.git
cd yarn-plugin
make setup
make start
make migrate   # applies the new techniques table alongside existing ones
```

A Ravelry API key/credential must be configured (env var, name TBD in tasks) before the pattern
endpoint can return real results — see research.md #1.

## Validació end-to-end

### 1. Recomanació de patrons (Ravelry en viu)
```bash
curl "http://localhost:8000/recommendations/patterns?query=cozy+beginner+sweater"
# → {"results": [{"name": ..., "category": "sweater", "difficulty": "beginner",
#     "craft_type": "knit", "source_url": "https://www.ravelry.com/patterns/...",
#     "required_technique_names": [...]}], "total": N, "message": "..."}
```

### 2. Sense resultats — resposta honesta
```bash
curl "http://localhost:8000/recommendations/patterns?query=nonexistent+pattern+xyz123"
# → {"results": [], "total": 0, "message": "No patterns found matching your query"}
```

### 3. Ravelry no disponible — resposta honesta, no inventada
```bash
# amb Ravelry simulat com a caigut (fixture/mock a l'entorn de test)
curl "http://localhost:8000/recommendations/patterns?query=sweater"
# → 503, missatge explícit que el servei de patrons no està disponible temporalment
```

### 4. Registrar una tècnica (admin, seed manual del catàleg propi)
```bash
curl -X POST http://localhost:8000/admin/techniques \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Purl stitch",
    "craft_type": "knit",
    "instructions": "1. Insert the needle... 2. Wrap the yarn... 3. Pull through...",
    "description": "One of the two basic knit stitches, alongside knit stitch."
  }'
# → 201 amb la tècnica creada
```

### 5. Consulta d'una tècnica
```bash
curl "http://localhost:8000/recommendations/techniques?query=how+do+I+purl"
# → {"results": [{"name": "Purl stitch", "craft_type": "knit", "instructions": "..."}],
#     "total": 1, "message": "..."}
```

### 6. Tècnica ambigua entre knit i crochet
```bash
curl "http://localhost:8000/recommendations/techniques?query=chain"
# → tots dos resultats (knit i crochet) si n'hi ha, o petició d'especificar craft_type —
#    mai només un sense indicar-ho (spec US2, acceptance scenario 2)

curl "http://localhost:8000/recommendations/techniques?query=chain&craft_type=crochet"
# → nomès el resultat de crochet
```

### 7. Documentació OpenAPI interactiva
Obre `http://localhost:8000/docs` al navegador — hauria d'incloure ara `/recommendations/patterns`
i `/recommendations/techniques`.

## Validació de qualitat
```bash
make qa      # lint + typecheck + arch-check + tests (90% cobertura)
```

Els tests de l'adapter de Ravelry (`ravelry_pattern_repository`) fan servir fixtures HTTP gravades —
`make qa` NO ha de dependre de tenir credencials reals de Ravelry ni de connectivitat externa.