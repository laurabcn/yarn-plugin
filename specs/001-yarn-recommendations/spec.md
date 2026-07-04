# Feature Specification: Yarn & Pattern Recommendations

**Feature Branch**: `001-yarn-recommendations`

**Created**: 2026-07-02

**Status**: Draft

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Yarn Recommendation by Natural Language Query (Priority: P1)

A user (via an AI assistant) asks a question in natural language about yarn. The system returns a ranked list of yarn recommendations with enough context for the AI to give a useful answer.

**Why this priority**: This is the core value proposition of the product. Without this, nothing else makes sense.

**Independent Test**: Ask "What yarn do you recommend for a beginner knitting a sweater?" and verify the system returns at least one yarn with name, weight, recommended use, and brand.

**Acceptance Scenarios**:

1. **Given** a query "best yarn for beginners", **When** the API receives it, **Then** it returns a list of yarns suitable for beginners, each with name, brand, weight, and a short description.
2. **Given** a query with no matching yarns, **When** the API receives it, **Then** it returns an empty list and a clear message explaining no results were found — it does NOT invent recommendations.
3. **Given** a vague query "something soft", **When** the API receives it, **Then** it returns yarns tagged with "soft" or similar attributes.

---

### User Story 2 — Pattern Recommendation by Natural Language Query (Priority: P2)

A user (via an AI assistant) asks for knitting pattern recommendations. The system returns relevant patterns with enough detail for the AI to present them.

**Why this priority**: Patterns are the second most common query type after yarn. Many users look for both together.

**Independent Test**: Ask "best knitting patterns for a chunky sweater" and verify the system returns at least one pattern with name, difficulty level, yarn weight, and author.

**Acceptance Scenarios**:

1. **Given** a query "cozy sweater patterns for winter", **When** the API receives it, **Then** it returns patterns tagged with sweater + winter/cozy attributes, with difficulty and required yarn type.
2. **Given** a query specifying difficulty "easy patterns for beginners", **When** the API receives it, **Then** it returns only patterns marked as beginner-friendly.

---

### User Story 3 — Brand Registration (Priority: P3)

A yarn brand or pattern designer registers their products so they appear in recommendations.

**Why this priority**: Without data, the system has nothing to recommend. But for MVP, we can seed data manually — user registration can come later.

**Independent Test**: A brand can submit their yarn details via the API and the yarn subsequently appears in relevant recommendation queries.

**Acceptance Scenarios**:

1. **Given** a brand submits a new yarn with name, weight, fiber content, and tags, **When** the submission is accepted, **Then** the yarn appears in relevant recommendation queries within the same session.

---

### User Story 4 — Stitch/Technique How-To (Priority: P3)

A user (via an AI assistant) asks how to perform a specific knitting or crochet technique — e.g. "how do I do a purl stitch" or "how do I make a chain stitch in crochet" — and receives accurate, step-by-step instructions for that specific technique and craft type, independent of any pattern.

**Why this priority**: Valuable on its own — many users look up "how to" technique instructions without following a specific pattern. Added in the same iteration as Pattern (US2) since both are curated, locally-owned catalog data with no external dependency, but scoped as its own story since a user can get value from it without Pattern existing.

**Independent Test**: Ask "how do I purl" and verify the system returns that technique's step-by-step instructions and craft type — deliverable without Pattern (US2) existing.

**Acceptance Scenarios**:

1. **Given** a catalog with a "purl stitch" (knit) technique, **When** a user asks "how do I purl", **Then** the system returns that technique's step-by-step instructions and craft type.
2. **Given** the same technique name exists in both knit and crochet vocabularies (e.g. "chain"), **When** a user's request doesn't specify which craft, **Then** the system either asks for the craft type or returns both, but never silently guesses and presents one as the only answer.
3. **Given** a catalog with no technique matching the request, **When** a user asks for a technique not in the catalog, **Then** the system clearly states no match was found rather than inventing instructions.

---

### Edge Cases

- What happens when the query is in a language other than English? → Return results in English, document limitation.
- What if two yarns are equally relevant? → Return both, ranked by data completeness.
- What if a brand submits duplicate yarn entries? → Deduplicate by name + brand.
- What happens when a technique name is ambiguous across knit and crochet (e.g. "chain")? → Both crafts are considered; results are not narrowed to one craft unless the user specifies it.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST accept a natural language query and return a ranked list of yarn recommendations.
- **FR-002**: The system MUST accept a natural language query and return a ranked list of pattern recommendations.
- **FR-003**: Each yarn recommendation MUST include: name, brand, weight category, fiber content, short description, and relevant tags.
- **FR-004**: Each pattern recommendation MUST include: name, author/designer, difficulty level, required yarn weight, and short description.
- **FR-005**: The system MUST return an empty result with an explanatory message when no matching items are found — it MUST NOT invent or hallucinate recommendations.
- **FR-006**: The system MUST expose its capabilities via an OpenAPI spec compatible with MCP and GPT Actions.
- **FR-007**: Brands and designers MUST be able to register their yarns and patterns via the API.
- **FR-008**: The system MUST allow querying stitch/technique how-to instructions via free-form natural language text or a technique name, returning real, existing techniques from our own curated catalog — never fabricated instructions.
- **FR-009**: Each technique MUST include, at minimum: name, craft type (knit or crochet), and step-by-step instructions.
- **FR-010**: The system MUST distinguish techniques by craft type where the same or a similar name exists in both knit and crochet vocabularies, never returning the wrong craft's instructions as if unambiguous.

### Key Entities

- **Yarn**: name, brand, weight (lace/fingering/DK/worsted/bulky/super-bulky), fiber content, tags (beginner-friendly, washable, natural, etc.), description.
- **Pattern**: name, designer, difficulty (beginner/intermediate/advanced), yarn weight required, category (sweater/hat/socks/etc.), tags, description.
- **Brand**: name, website, description.
- **Technique** (a.k.a. Stitch): a reusable, named knitting or crochet skill (e.g. "purl stitch", "chain stitch"), independent of any pattern. Has a name, craft type (knit/crochet), and step-by-step instructions. Curated/seeded catalog data, same as Yarn/Pattern/Brand — no external dependency.
- **Query**: the natural language text used to search — not persisted, used only at runtime.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A query returns relevant results in under 2 seconds.
- **SC-002**: At least 80% of test queries return at least one relevant result when the catalogue has 20+ yarns.
- **SC-003**: An AI assistant using this API can answer yarn questions without inventing brand names or specifications.
- **SC-004**: A brand can register a new yarn and it appears in relevant queries without manual intervention.
- **SC-005**: A user can get accurate, step-by-step instructions for a named technique from a single request, without needing to search external sites.

## Assumptions

- For MVP, the catalogue is seeded manually — a public self-registration flow is a future feature.
- Queries are in English; multilingual support is out of scope for v1.
- Relevance ranking is keyword and tag-based for v1; semantic search (embeddings) is a future enhancement.
- Authentication for brand registration is out of scope for v1 — the endpoint is internal/admin only.
- The API is consumed by AI assistants, not directly by end users — no UI is needed in this repo.
