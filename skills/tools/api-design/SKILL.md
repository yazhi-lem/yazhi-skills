---
name: api-design
description: Use when designing a new REST or RPC API surface, or reviewing an existing one for consistency — resource naming, versioning, pagination, error shapes, and backward compatibility. Helps you avoid the breaking-change and inconsistency traps that make an API painful for every client that integrates against it.
---

An API is a contract you'll be living with long after the code that first implemented it is gone, so the cost of an inconsistency compounds across every client that has to special-case it. Fix naming, pagination, and error shape conventions once, up front, and apply them uniformly rather than deciding per-endpoint.

## Workflow

1. **Name resources as plural nouns, not verbs.** `/orders`, `/orders/{id}/items` — never `/getOrders` or `/createOrder`. Actions that don't fit CRUD become sub-resources or a POST with a verb suffix (`/orders/{id}/cancel`), used sparingly.
2. **Pick a versioning strategy before the first external consumer, not after.** URI versioning (`/v1/orders`) is the simplest to reason about and cache; header-based versioning is more "correct" but harder to debug in a browser or curl. Default to URI versioning unless you have a specific reason not to.
3. **Paginate every list endpoint from day one**, even if you're sure the list will stay small — retrofitting pagination breaks clients. Default page size 20-50, cursor-based (opaque `next_cursor`) over offset-based for anything with concurrent writes.
4. **Support idempotency keys on every unsafe POST that creates a resource.** Client sends `Idempotency-Key` header; server dedupes for a bounded window (default 24h) and returns the original response on retry. This is what makes client-side retry-on-timeout safe.
5. **Standardize one error response shape across the entire API** (see table) and use it for every 4xx/5xx, no exceptions per-endpoint.
6. **Define your backward-compatibility bar explicitly**: adding an optional field or a new endpoint is non-breaking; removing/renaming a field, changing a type, or tightening validation is breaking and requires a new version. Write this down so reviewers don't relitigate it per PR.
7. **Deprecate with a timeline, not a silent removal.** Add a `Deprecation`/`Sunset` header or changelog entry with a concrete date, minimum 90 days out for anything with external consumers.

## Error response shape

| Field | Type | Purpose |
|---|---|---|
| `error.code` | string, stable enum | Machine-matchable identifier (`resource_not_found`), never changes across versions |
| `error.message` | string | Human-readable, safe to display, no stack traces or internal ids |
| `error.details` | array/object, optional | Field-level validation errors (`{field: "email", issue: "invalid_format"}`) |
| `request_id` | string | Correlates client report to server logs |
| HTTP status | int | Matches semantics: 400 validation, 401/403 auth, 404 not found, 409 conflict, 422 semantic error, 429 rate limit, 5xx server fault |

Numeric defaults worth standardizing: 50 max page size (cap it — don't let clients request unbounded pages), 30s server-side request timeout, 429 responses carry a `Retry-After` header, rate limits default to something generous enough not to throttle normal pagination (e.g., 100 req/min per key) with room to raise per-client.

## Anti-patterns

- **Verb-shaped endpoints mixed with resource-shaped ones.** `/getUser` next to `/orders/{id}` — pick REST resource semantics and stay consistent, or go full RPC (`/rpc/getUser`) and stay consistent; don't blend.
- **Breaking changes shipped as "the same version."** Adding a required field, changing a field's type, or altering error codes without bumping the version — this silently breaks every existing client at once.
- **Offset pagination on a frequently-written table.** Causes skipped or duplicated rows as the underlying data shifts mid-pagination; use cursor-based pagination instead.
- **Inconsistent error shapes per endpoint or per team.** Forces every client to write bespoke error-parsing logic instead of one shared handler.
- **No idempotency story for retries.** Client times out, retries a POST, and creates a duplicate resource — idempotency keys are the fix, not "tell clients not to retry."

If this API is also going to be exposed as tools an LLM calls directly, read `mcp-server-development` too — the same resource, but the shape constraints differ (verbose JSON that's fine for a typed SDK client is expensive for a model to read). See `cli-tool-design` if a CLI wraps this API — its `--json` mode should mirror this same error and pagination shape for consistency.
