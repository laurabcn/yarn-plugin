# Research: User Access (Invite-Only)

## Decisions

### 1. JWT amb python-jose

**Decision**: `python-jose[cryptography]` per a JWT encode/decode.

**Rationale**: Llibreria estàndard per a JWT en FastAPI. Lleuger, ben documentat, compatible amb RS256 i HS256. Per a v1 usem HS256 amb secret simètric.

**Alternatives considerades**:
- `PyJWT` → similar, però python-jose té millor integració amb l'ecosistema FastAPI
- Sessions + cookies → descartada, l'API és consumida per IAs i CLIs, no navegadors

---

### 2. bcrypt amb passlib

**Decision**: `passlib[bcrypt]` per a hash de passwords.

**Rationale**: bcrypt és l'estàndard per a passwords — lent per disseny (dificulta brute force), salt automàtic, àmpliament provat. `passlib` abstreu la implementació.

**Alternatives considerades**:
- argon2 → més modern, però bcrypt té més suport i és suficient per v1
- SHA-256 → descartada, mai per a passwords (massa ràpid)

---

### 3. Admin auth per secret estàtic

**Decision**: El header `X-Admin-Secret` comparat amb `ADMIN_SECRET` de l'entorn.

**Rationale**: L'admin és una sola persona (la propietària del sistema). Un compte d'admin amb JWT seria sobreenginyeria. El secret estàtic és simple, segur en producció amb HTTPS, i fàcil de rotar.

**Alternatives considerades**:
- Compte admin amb JWT → descartada (YAGNI en v1)
- HTTP Basic Auth → possible però menys explícit

---

### 4. Token d'invitació com a UUID aleatori

**Decision**: El token d'invitació és un `secrets.token_urlsafe(32)` — 43 caràcters URL-safe.

**Rationale**: Criptogràficament segur, prou llarg per evitar enumeració, URL-safe sense encoding addicional.

**Alternatives considerades**:
- JWT com a token d'invitació → innecessari, el token no porta payload, és un simple secret
- UUID4 → menys entropy que `token_urlsafe`
