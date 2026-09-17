---
name: tamil-social-content
description: Use when social media content needs to be produced or adapted in Tamil — either the request explicitly asks for Tamil copy, or asks for a Tamil version alongside an English one. Bridges the social-media pipeline to the repo's existing `tamil-content-writing` skill so Tamil output is natural and idiomatic, not a mechanical translation.
---

This skill ensures Tamil social media copy goes through the repo's existing `tamil-content-writing` skill — which already handles idiomatic phrasing and avoids literal English-calque translation — rather than being produced as a direct word-for-word translation of the English draft. This skill does not duplicate `tamil-content-writing`'s logic; it applies it in the specific context of finished social copy.

## Step 1 — Draft in base language first

Run the normal pipeline (`social-caption-writing` or `reel-script-generation`, then `tone-of-voice-application`) to produce the finished English copy first. Tamil adaptation happens on the finished, brand-voice-approved draft — not on a rough first draft — so tone and structure are already locked before translation begins.

## Step 2 — Adapt, don't translate

Hand the finished English copy to `tamil-content-writing` with instructions to adapt the *meaning and intent*, not the sentence structure. Apply these checks:

| Check | Fail pattern | Pass pattern |
|---|---|---|
| Idiom vs. calque | Word-for-word rendering of an English idiom into Tamil | A natural Tamil expression carrying the same meaning |
| Sentence rhythm | Tamil sentence forced into English word order | Tamil sentence reads the way Tamil is actually spoken/written |
| Brand voice preserved | Directness lost in translation (softened, hedged) | Bold/direct tone carried into Tamil phrasing |
| Numerals | Mixed or inconsistent digit style | Western numerals used consistently, per standard social media convention |

## Step 3 — Decide on code-mixing (Tanglish)

Ask, or infer from platform and audience, whether the post should be:
1. **Pure Tamil script** — formal announcements, LinkedIn, educational content
2. **Tamil with English technical terms retained** — product/technical terms often stay in English even in Tamil copy (e.g. brand names, "AI," "cloud") rather than being forced into Tamil equivalents that readers won't recognize
3. **Tanglish (Latin-script Tamil)** — casual platforms (Instagram, reels) where the audience commonly reads romanized Tamil

Default to option 2 (Tamil with retained English technical terms) unless the brief specifies otherwise.

## Step 4 — Hashtags

Keep hashtags in English even on Tamil posts, unless the brand has an established Tamil hashtag campaign — English hashtags remain far more discoverable across platforms and are standard practice even for Tamil-language content.

## Step 5 — Output format

Produce both versions side by side so the team can choose or publish both:

```text
PLATFORM: <name>
LANGUAGE: Tamil (script) / Tamil (Tanglish) — specify which
---
ENGLISH DRAFT:
<approved English copy>

TAMIL ADAPTATION:
<Tamil copy, adapted not translated>
---
HASHTAGS: #tag1 #tag2 #tag3
NOTES: <code-mixing decision made, any terms kept in English and why>
```

## Common failure modes

- **Literal translation instead of adaptation**: running the English copy through a direct translator rather than `tamil-content-writing`'s idiomatic approach, producing grammatically correct but unnatural Tamil that reads as obviously translated.
- **Losing brand voice in translation**: a bold, direct English post becoming softened or formal-sounding in Tamil because directness doesn't map 1:1 across languages without deliberate word choice.
- **Forcing English technical terms into awkward Tamil equivalents**: translating terms like "cloud" or "AI" into constructed Tamil words the audience won't recognize, instead of retaining the English term as is common practice in technical Tamil writing.
- **Skipping the code-mixing decision**: defaulting to pure Tamil script for a casual Instagram/reel audience that actually reads and expects Tanglish, reducing engagement.
