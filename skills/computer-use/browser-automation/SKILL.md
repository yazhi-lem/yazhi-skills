---
name: browser-automation
description: Use when an agent must drive a real or headless browser (Playwright, Puppeteer, Selenium) to fill forms, scrape dynamic content, or verify a web flow end-to-end. Helps you pick robust selectors, wait strategies, and verification steps so the automation survives layout changes and network variance.
---

Browser automation fails most often not because the tool is weak but because the script assumes a static DOM and instant network responses. Treat every page as a moving target: elements load asynchronously, layouts shift under A/B tests, and sessions expire mid-run. Favor the accessibility tree over visual layout whenever the driver supports it (e.g. Playwright's `browser_snapshot` role/name queries beat raw CSS).

## Workflow

1. **Establish state first.** Navigate, then wait for a concrete signal (a specific element visible, `networkidle`, or a data attribute) — never wait for a fixed sleep alone. Default: 10s navigation timeout, 5s per-action timeout, 3 retries with exponential backoff (500ms, 1500ms, 4000ms).
2. **Resolve the selector using the priority order below** before falling back to CSS.
3. **Act, then re-verify.** After every click/type/submit, take a snapshot or screenshot and confirm the expected post-condition (URL changed, toast appeared, row count incremented) rather than assuming the action succeeded.
4. **Handle auth up front.** Reuse a persisted storage state (cookies/localStorage) instead of re-logging-in per run; refresh it only when a session-expired signal is detected (redirect to `/login`, 401 response, or a specific DOM marker).
5. **Isolate dynamic content.** For infinite scroll, polling widgets, or websockets, poll for the target condition with a bounded loop (e.g. check every 500ms, max 20 attempts = 10s) instead of a single wait.
6. **Screenshot-verify at checkpoints**, not every step — before/after a multi-field form submit, after navigation, and on any failure, to keep the evidence trail small but diagnostic.
7. **Clean up sessions and tabs** explicitly at the end of a run; leaked browser contexts cause flaky parallel runs.

## Selector strategy comparison

| Strategy | Robustness | When to use | Avoid when |
|---|---|---|---|
| Role + accessible name (`getByRole`) | High | Buttons, links, form fields with labels | Element has no semantic role (custom canvas widgets) |
| `data-testid` / `data-qa` attributes | High | App code you control and can annotate | Third-party pages you can't modify |
| Text content (`getByText`) | Medium | Unique, stable copy (button labels) | Copy is localized or A/B tested |
| CSS class/structure | Low | Last resort, quick scripts | Any production automation — classes churn with styling refactors |
| Absolute XPath | Very low | Never for production | Breaks on any DOM reorder |

## Numeric defaults

- Navigation timeout: 10s; action timeout: 5s; assertion/poll timeout: 5s.
- Retry count: 3 attempts per action with exponential backoff, cap at 4s.
- Screenshot on: navigation, form submit, and every failure (not every step).
- Session/auth-state TTL check: revalidate if idle > 15 minutes before reuse.
- Max poll loop: 20 iterations at 500ms for dynamic content waits.

## Anti-patterns

- **Fixed `sleep(n)` instead of condition-based waits** — either too slow (wastes time) or too fast (flakes under load); always wait on a signal.
- **XPath/CSS selectors tied to DOM position** (`div > div:nth-child(3) > span`) — breaks the moment a designer adds a wrapper div.
- **Re-authenticating every run** — slow, and often trips bot/rate-limit detection; persist and reuse session state instead.
- **Assuming an action succeeded because no exception was thrown** — clicks can silently no-op on overlapping elements; always verify the post-condition.
- **Scraping rendered text for state that's available in the accessibility tree or an API response** — the accessible-name/role tree is far more stable across visual redesigns than text scraping.

For agents that also need to decide *what* to click based on ambiguous natural-language instructions, see `gui-agent-design`. For workflows spanning the browser plus native apps or the filesystem, see `desktop-workflow-automation`.
