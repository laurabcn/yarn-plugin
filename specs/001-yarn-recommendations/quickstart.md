# Quickstart & Validation Guide

## Prerequisites

```bash
git clone https://github.com/laurabcn/yarn-plugin.git
cd yarn-plugin
make setup
make start
make migrate
```

## Validació end-to-end

### 1. Health check
```bash
curl http://localhost:8000/health
# → {"status": "ok"}
```

### 2. Registrar una llana (admin)
```bash
curl -X POST http://localhost:8000/admin/yarns \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Drops Alaska",
    "brand_name": "Drops",
    "weight": "worsted",
    "fiber_content": "100% wool",
    "description": "Rustic Norwegian wool, great for warm garments",
    "tags": ["beginner-friendly", "natural", "warm", "washable"]
  }'
# → 201 amb el yarn creat
```

### 3. Recomanació de llanes
```bash
curl "http://localhost:8000/recommendations/yarn?query=best+yarn+for+beginners"
# → {"results": [...], "total": 1, "message": "Found 1 yarn matching your query"}
```

### 4. Sense resultats — resposta honesta
```bash
curl "http://localhost:8000/recommendations/yarn?query=silk+yarn+for+lace"
# → {"results": [], "total": 0, "message": "No yarns found matching your query"}
```

### 5. Documentació OpenAPI interactiva
Obre `http://localhost:8000/docs` al navegador.

## Validació de qualitat
```bash
make qa      # lint + typecheck + arch-check + tests (90% cobertura)
```
