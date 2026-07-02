# Feature Specification: User Access (Invite-Only)

**Feature Branch**: `002-user-access`

**Created**: 2026-07-02

**Status**: Draft

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Admin Creates and Sends an Invitation (Priority: P1)

The admin (system owner) creates an invitation for a new user (a yarn brand, a pattern designer like Katia). The system generates a unique invite link with an expiry date. The admin shares it manually (email, Telegram, etc.).

**Why this priority**: Without invitations, no new users can join. Everything else depends on this.

**Independent Test**: Admin calls `POST /admin/invitations` and receives a unique invite token and link. The token can be verified as valid.

**Acceptance Scenarios**:

1. **Given** the admin calls `POST /admin/invitations` with an email, **When** the request is accepted, **Then** the system returns a unique invite token valid for 7 days.
2. **Given** an invitation has been created, **When** the admin calls `GET /admin/invitations`, **Then** the invitation appears in the list with its status (pending/accepted/expired).
3. **Given** an invitation has expired (>7 days), **When** someone tries to use it, **Then** the system rejects it with a clear error message.

---

### User Story 2 — New User Accepts Invitation and Creates Account (Priority: P2)

A person who received an invite link opens it and creates their account by setting a password. After that they can log in.

**Why this priority**: The invite is useless without the acceptance flow.

**Independent Test**: `POST /auth/accept-invitation` with a valid token and a password creates a user and returns a success confirmation.

**Acceptance Scenarios**:

1. **Given** a valid unused invite token, **When** the user submits it with a chosen password, **Then** their account is created and the invitation is marked as accepted.
2. **Given** an already-used invite token, **When** someone tries to use it again, **Then** the system rejects it — each invitation is single-use.
3. **Given** a valid token, **When** the user submits a password shorter than 8 characters, **Then** the system rejects it with a validation error.

---

### User Story 3 — User Logs In and Gets Access Token (Priority: P3)

A registered user logs in with their email and password and receives a JWT token they can use to call protected endpoints.

**Why this priority**: Without login, authenticated users can't submit content.

**Independent Test**: `POST /auth/login` with valid credentials returns a JWT token. Using that token on a protected endpoint returns 200, not 401.

**Acceptance Scenarios**:

1. **Given** a registered user, **When** they submit correct email + password, **Then** they receive a JWT token valid for 24 hours.
2. **Given** a registered user, **When** they submit wrong credentials, **Then** the system returns 401 — it does NOT reveal whether the email exists.
3. **Given** a valid JWT token, **When** it is included in a request to a protected endpoint, **Then** the request is processed normally.
4. **Given** an expired or invalid JWT token, **When** it is included in a request, **Then** the system returns 401.

---

### Edge Cases

- What if the admin sends two invitations to the same email? → Both are valid until used. The second accepted one wins.
- What if a user forgets their password? → Out of scope for v1 — admin can create a new invitation.
- What if the JWT secret changes? → All existing tokens are invalidated — documented behaviour.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST allow the admin to create invite-only invitations via a protected endpoint.
- **FR-002**: Each invitation MUST have a unique token and expire after 7 days.
- **FR-003**: Each invitation MUST be single-use — once accepted it cannot be used again.
- **FR-004**: The system MUST allow a user to accept an invitation and create an account with a password.
- **FR-005**: Passwords MUST be stored hashed — never in plain text.
- **FR-006**: The system MUST allow registered users to log in with email + password and receive a JWT token.
- **FR-007**: Protected endpoints MUST reject requests without a valid JWT token with a 401 response.
- **FR-008**: The admin endpoint for creating invitations MUST be protected by a static admin secret (environment variable), not by JWT — the admin has no account in the system.

### Key Entities

- **User**: id (UUID), email, password_hash, created_at, invitation_id (FK).
- **Invitation**: id (UUID), email, token (unique string), expires_at, accepted_at (nullable), created_by (admin).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: An admin can create an invitation and a new user can register in under 2 minutes end-to-end.
- **SC-002**: A protected endpoint returns 401 for 100% of requests without a valid JWT token.
- **SC-003**: Login response time is under 1 second for valid credentials.
- **SC-004**: Passwords are never stored or logged in plain text — verifiable by database inspection.

## Assumptions

- The admin is a single person (the system owner) identified by a static secret in `.env` — no admin account needed.
- Password reset is out of scope for v1 — admin creates a new invitation.
- Email sending is out of scope for v1 — the admin copies and sends the invite link manually.
- JWT tokens are stateless — no token revocation in v1.
- A single user role exists — all registered users have the same permissions (can submit yarns/patterns).
- HTTPS is assumed in production — HTTP is acceptable for local development only.
