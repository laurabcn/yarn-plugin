# Quickstart & Validation Guide — User Access

## Prerequisites

```bash
make start && make migrate
export ADMIN_SECRET=supersecret  # o defineix-lo a .env
```

## Validació end-to-end

### 1. Admin crea una invitació
```bash
curl -X POST http://localhost:8000/admin/invitations \
  -H "X-Admin-Secret: supersecret" \
  -H "Content-Type: application/json" \
  -d '{"email": "katia@example.com"}'
# → 201 amb token, invite_url i expires_at
# invite_url és el link complet que l'admin envia a l'usuari per email/WhatsApp/etc.
# Exemple: "http://localhost:3000/accept?token=abc123..."
```

### 1b. Frontend valida el token (abans de mostrar el formulari)
```bash
curl http://localhost:8000/auth/invitation/<TOKEN>
# → 200: {"email": "katia@example.com", "expires_at": "..."}  (formulari visible)
# → 400: token expirat o ja usat
# → 404: token no trobat
```

### 2. Usuari accepta la invitació
```bash
curl -X POST http://localhost:8000/auth/accept-invitation \
  -H "Content-Type: application/json" \
  -d '{"token": "<TOKEN_DEL_PAS_1>", "password": "mysecurepassword"}'
# → 201: "Account created successfully"
```

### 3. Usuari fa login
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "katia@example.com", "password": "mysecurepassword"}'
# → 200 amb access_token JWT
```

### 4. Endpoint protegit amb JWT
```bash
curl -X POST http://localhost:8000/yarns \
  -H "Authorization: Bearer <JWT_DEL_PAS_3>" \
  -H "Content-Type: application/json" \
  -d '{"name": "Drops Alaska", ...}'
# → 201 (en lloc de 401 sense token)
```

### 5. Errors esperats
```bash
# Token ja usat
curl -X POST http://localhost:8000/auth/accept-invitation \
  -d '{"token": "<TOKEN_JA_USAT>", "password": "test1234"}'
# → 400: "Invitation already used"

# Credencials incorrectes
curl -X POST http://localhost:8000/auth/login \
  -d '{"email": "katia@example.com", "password": "wrong"}'
# → 401 (sense revelar si l'email existeix)

# Sense JWT en endpoint protegit
curl -X POST http://localhost:8000/yarns -d '{...}'
# → 401
```

## Validació de qualitat
```bash
make qa
```
