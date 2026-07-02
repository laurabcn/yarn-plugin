# Data Model: User Access

## Entities

### Invitation

| Camp | Tipus | Restriccions |
|---|---|---|
| id | UUID | PK, auto-generat |
| email | string | NOT NULL |
| token | string | NOT NULL, únic, 43 chars URL-safe |
| expires_at | timestamp | NOT NULL (created_at + 7 dies) |
| accepted_at | timestamp | nullable — null = pendent |
| created_at | timestamp | NOT NULL |

**Regles**:
- `token` ha de ser únic a la taula
- `accepted_at` null → invitació pendent; no-null → ja usada
- `expires_at < now()` → invitació expirada (rebutjar fins i tot si `accepted_at` és null)

---

### User

| Camp | Tipus | Restriccions |
|---|---|---|
| id | UUID | PK, auto-generat |
| email | string | NOT NULL, únic |
| password_hash | string | NOT NULL |
| invitation_id | UUID | FK → Invitation, NOT NULL |
| created_at | timestamp | NOT NULL |

**Regles**:
- `email` ha de ser únic
- `password_hash` mai es retorna en cap resposta
- `invitation_id` traça l'origen de cada compte

---

## Relacions

```
Invitation 1 ──── 0..1 User
```

## Notes

- Els IDs són UUIDs generats a la capa d'aplicació (domini controla la identitat).
- `password_hash` s'omple a la capa d'infraestructura (`PasswordService`) — el domini no coneix bcrypt.
- El domini valida les regles de negoci (token expirat, token ja usat) però no el hashing.
