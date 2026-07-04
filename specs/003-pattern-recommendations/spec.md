# Feature Specification: Pattern & Stitch Recommendations

**Feature Branch**: `003-pattern-recommendations`

**Created**: 2026-07-03

**Status**: Superseded (2026-07-04) — the "Pattern sourced live from Ravelry" design (US1) was reverted
after reconsidering MVP scope and latency/reliability of live third-party queries. `Pattern` reverts to
`001-yarn-recommendations`'s original local/curated design (Phase 4, T024-T033 — same recipe as `Yarn`),
which was never implemented and is now the active plan. This spec's User Story 2 (Technique how-to) and
its underlying decision (own curated catalog, unaffected by the Pattern reversal) may still be picked up
later — see the open question left for the user in this session about whether to keep it as a separate
feature or fold it into 001's scope.

**Input**: User description: "Add pattern recommendations and knitting/crochet stitch (technique) recommendations. Users should be able to ask for pattern recommendations (e.g. 'recommend a beginner sweater pattern') similar to the existing yarn recommendations endpoint. Additionally, add a separate concept for stitch/technique how-tos (e.g. 'how do I do a purl stitch' or 'how do I make a chain stitch in crochet') — these are reusable techniques that patterns may reference, distinct from a full pattern."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Get a pattern recommendation (Priority: P1)

A user (directly, or via an AI assistant like Claude acting on their behalf) describes what they want to make in plain language — e.g. "a beginner-friendly sweater" or "a quick baby blanket" — and receives real pattern recommendations sourced live from an external, third-party pattern index (Ravelry), instead of an invented suggestion. The system never stores or republishes the third-party pattern content itself — it looks it up on demand and relays it, with attribution back to the source.

**Why this priority**: This is the core value proposition of the whole product (per the project's mission): give an AI assistant real data instead of letting it hallucinate. Patterns are the second half of that promise, after yarn. Sourcing live from an established pattern index also sidesteps hosting copyrighted design content ourselves.

**Independent Test**: Can be fully tested by querying pattern recommendations with a natural-language description and verifying the returned patterns are real, structured records (not free text) with category, difficulty, craft type, and a source attribution/link — deliverable and demonstrable without the technique feature existing yet.

**Acceptance Scenarios**:

1. **Given** the external pattern index has a beginner-level hat pattern, **When** a user asks for "a simple hat for a beginner", **Then** the system returns that pattern with its category, difficulty, craft type, and a link back to the source.
2. **Given** no pattern in the external index matches the request, **When** a user asks for something with no match (e.g. "an advanced lace wedding shawl"), **Then** the system clearly states no match was found rather than returning an unrelated or fabricated pattern.
3. **Given** a pattern that requires specific techniques to complete, **When** a user views that pattern's recommendation, **Then** the required techniques are listed by name alongside it, where the external source provides that information.
4. **Given** the external pattern index is unavailable or errors out, **When** a user requests a pattern recommendation, **Then** the system clearly states the recommendation service is temporarily unavailable rather than fabricating a result or failing silently.

---

### User Story 2 - Get a stitch/technique how-to (Priority: P2)

A user asks how to perform a specific knitting or crochet technique — e.g. "how do I do a purl stitch" or "how do I make a chain stitch in crochet" — and receives accurate, step-by-step instructions for that specific technique and craft type.

**Why this priority**: Valuable on its own (independent of patterns) — many users look up "how to" technique instructions without following a specific pattern. It also unblocks User Story 3.

**Independent Test**: Can be fully tested by querying a technique by name (e.g. "purl stitch", craft type knit) and verifying step-by-step instructions are returned — deliverable and demonstrable without any pattern data existing.

**Acceptance Scenarios**:

1. **Given** a catalog with a "purl stitch" (knit) technique, **When** a user asks "how do I purl", **Then** the system returns that technique's step-by-step instructions and craft type.
2. **Given** the same technique name exists in both knit and crochet vocabularies (e.g. "chain"), **When** a user's request doesn't specify which craft, **Then** the system either asks for the craft type or returns both, but never silently guesses and presents one as the only answer.
3. **Given** a catalog with no technique matching the request, **When** a user asks for a technique not in the catalog, **Then** the system clearly states no match was found rather than inventing instructions.

---

### User Story 3 - See which techniques a pattern requires (Priority: P3)

A user reviewing a recommended pattern wants to know, before starting, whether they already know the techniques it needs — cross-referencing a pattern's required techniques with the technique how-to catalog from User Story 2.

**Why this priority**: Builds on both prior stories; nice-to-have that ties the catalog together, but the product delivers value without it (a user can still look up a technique by name manually).

**Independent Test**: Can be tested by taking a pattern that lists required techniques and verifying each listed technique name resolves to a real technique record with instructions — requires both US1 and US2 to exist first.

**Acceptance Scenarios**:

1. **Given** a pattern that requires "purl stitch" and "cast on", **When** a user requests that pattern's recommendation, **Then** both technique names are returned as structured references, not free text, resolvable against the technique catalog.

### Edge Cases

- What happens when a pattern references a technique that doesn't (yet) exist in our technique catalog? The pattern is still returned; the missing technique reference is flagged rather than silently dropped or causing the whole recommendation to fail.
- How does the system handle a query that mixes both intents (e.g. "recommend a pattern that only uses stitches I already know: purl and knit")? Out of scope for v1 — treated as two separate queries (pattern recommendation, technique lookup); combined filtering is a future enhancement.
- How does the system handle craft-type-ambiguous pattern requests (e.g. "a scarf" without specifying knit or crochet)? Both crafts are considered; results are not filtered to one craft unless the user specifies it.
- What happens when the external pattern index is slow, rate-limits us, or is temporarily down? The system reports the recommendation as currently unavailable rather than hanging indefinitely or fabricating a substitute.
- What happens when the external index's data is incomplete for a given pattern (e.g. no listed techniques, or no difficulty rating)? The pattern is still returned with whatever fields are available; missing fields are omitted rather than guessed.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow querying pattern recommendations via free-form natural language text, sourcing results live from an external, third-party pattern index — never a fabricated one, and never a locally stored copy of the pattern's own content.
- **FR-002**: System MUST allow querying stitch/technique how-to instructions via free-form natural language text or a technique name, returning real, existing techniques from our own curated catalog — never fabricated instructions.
- **FR-003**: Each pattern recommendation MUST include, at minimum: name, category, difficulty level, craft type (knit or crochet), a link/attribution back to the external source, and the list of techniques it requires where the external source provides that information.
- **FR-004**: Each technique MUST include, at minimum: name, craft type (knit or crochet), and step-by-step instructions.
- **FR-005**: System MUST clearly and honestly state when no pattern or technique matches a query, consistent with the project's existing "never hallucinate" principle for yarn recommendations.
- **FR-006**: A pattern MAY reference zero or more techniques it requires; a technique MUST be independently queryable on its own, without requiring a pattern to reference it first.
- **FR-007**: System MUST distinguish techniques by craft type where the same or a similar name exists in both knit and crochet vocabularies, never returning the wrong craft's instructions as if they were unambiguous.
- **FR-008**: System MUST clearly and honestly state when the external pattern index is unavailable, rather than hanging indefinitely or returning a fabricated result.

### Key Entities

- **Pattern**: A knitting or crochet project a user can make (e.g. a sweater, hat, blanket), sourced live from an external, third-party pattern index rather than authored or stored by us. Represented by a name, category (already modeled as `PatternCategory`), difficulty level (already modeled as `Difficulty`), craft type, a source attribution/link, and the techniques it requires where known.
- **Technique** (a.k.a. Stitch): A reusable, named knitting or crochet skill (e.g. "purl stitch", "chain stitch") independent of any specific pattern, curated and owned by us (unlike Pattern). Has a name, craft type, and step-by-step instructions. Many patterns can reference the same technique.
- **CraftType**: Distinguishes knitting from crochet — needed because pattern and technique vocabularies differ by craft and the same name can mean different things in each.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A user can get a relevant pattern recommendation from a single natural-language request, without needing to know exact pattern names in advance, and always with a source attribution they can follow for the full pattern.
- **SC-002**: A user can get accurate, step-by-step instructions for a named technique from a single request, without needing to search external sites.
- **SC-003**: When no pattern or technique matches a request, or the external pattern index is unavailable, the system states this clearly instead of fabricating a result, in 100% of such cases.
- **SC-004**: For any pattern that lists required techniques, every listed technique name is verifiable as a real, resolvable technique record in our own catalog (no dangling references presented as valid).

## Assumptions

- Patterns are sourced live, on demand, from an external third-party pattern index (Ravelry) — we do not store, own, or republish their pattern content, only relay structured metadata with attribution. This requires access to that external service (API credentials/terms permitting) as an external dependency.
- Techniques are curated/seeded catalog data that we own (consistent with how Yarn and Brand already work) — no user-submitted content in this version.
- Technique instructions are plain text for this version; images or video are out of scope until there's a frontend to display them.
- "Craft type" covers knitting and crochet only for this version — other crafts (e.g. tunisian crochet as a distinct discipline, weaving) are out of scope unless explicitly requested later.
- A pattern's required techniques (as reported by the external index) are matched by name against our own technique catalog; a technique named by the external source that doesn't exist in our catalog is a known, acceptable gap (see Edge Cases), not a failure.