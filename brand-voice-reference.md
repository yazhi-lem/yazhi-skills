# Brand Tone-of-Voice Reference

This is the reference document the `tone-of-voice-application` skill applies
whenever it runs. If this file is present, it overrides the skill's default
voice rules.

---

## Brand Personality

**Bold, confident, direct.**

- Say the thing plainly. Don't hedge, don't soften a strong claim with "maybe" or "we think."
- Lead with the point, not the setup. Cut throat-clearing openers.
- Short, declarative sentences over long, qualifying ones.
- Confidence reads as competence — write like the company already knows it's right, backed by the facts in hand.

## Voice Do's

- Use active voice: "We built X" not "X was built by us"
- State claims directly: "This cuts deployment time in half" not "This could potentially help reduce deployment time"
- One idea per sentence. Break up anything doing two jobs.
- Use concrete numbers and specifics over vague qualifiers ("30% faster" beats "much faster")
- End posts with a direct, single call to action — no stacked asks

## Voice Don'ts

- **No emoji, ever.** Not even sparingly. This includes checkmark emoji (✅), thinking-face (💭), or any decorative symbol.
- No hedging language: avoid "might," "could potentially," "we think maybe," "it's possible that"
- No corporate filler: avoid "in today's fast-paced world," "at the end of the day," "synergy," "leverage" (as a verb), "circle back"
- No rhetorical questions as a crutch — if used, one per post maximum, and only if it's the actual hook
- No apologetic framing ("just wanted to," "sorry to bother")
- No exclamation points stacked for emphasis — one is plenty, most posts need zero

## Banned / Discouraged Words

| Avoid | Use instead |
|---|---|
| leverage (verb) | use |
| synergy | — (cut it) |
| game-changing | state the specific change |
| innovative | show what's actually new |
| seamless | state what specifically works well |
| disrupt / disruption | state what it replaces or improves |
| "we're excited to..." | just state the news |

## Sentence & Structure Rules

- Prefer sentences under 20 words. If a sentence needs a comma to hold two ideas, consider splitting it.
- Paragraphs: 1–3 sentences max for social copy.
- No emoji as bullet substitutes — use plain dashes or checkmarked words in text ("No foreign backdoors." not "✅ No foreign backdoors")

## Example Rewrite (before/after)

**Generic default voice:**
> Where is your AI actually thinking? 💭 Most popular AI tools send your data to servers overseas... Hit the link in our bio to learn how Sovereign AI works.

**Brand voice (bold/confident/direct, no emoji):**
> Most AI tools send your data overseas. You don't choose the server. You don't control the jurisdiction.
>
> Sovereign AI puts that back in your hands. Your data. Your models. Your infrastructure.
>
> No backdoors. No compliance gaps. No dependency on someone else's cloud.
>
> Read how it works — link in bio.

---

*Voice source note: when this document is used, `tone-of-voice-application` should output `VOICE SOURCE: brand-voice-reference.md` instead of "default voice rules used."*
