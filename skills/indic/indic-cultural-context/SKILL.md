---
name: indic-cultural-context
description: Use when content, product behavior, or research across Indian languages needs cultural review — names, regions, festivals, food, family terms, caste/community references, or humor. Helps you keep a living, sourced context register instead of relying on stereotypes; Tamil cultural accuracy stays with org-ethos.
---

# Indic Cultural Context

India is not one culture, and "Indian user" is not a persona. This skill owns the evolving, sourced register for cultural context across languages and regions. `org-ethos` owns the cultural-accuracy gate; this skill supplies the evidence a reviewer can check.

## Workflow

1. **Name the region and audience before the language.** Language alone does not determine context. A Hindi speaker in Delhi and one in a regional minority setting do not share the same references.
2. **Check the context register.** Look for an existing entry for the name, festival, food, family term, or idiom in the repo's living register. If none exists, open a sourced entry before using the reference in copy.
3. **Separate shared, regional, and community-specific references.** Mark each example accordingly. Shared references need broad testing; community-specific ones need a reviewer from that community.
4. **Avoid flattening identity.** Do not use caste, religion, region, or community as shorthand for character or behavior. If a reference is essential to the claim, say why and cite the source.
5. **Review humor and metaphor with a native speaker.** Jokes and idioms rarely survive literal transfer; a failed metaphor can turn an otherwise accurate sentence into an insult.
6. **Record the decision, not just the result.** The register entry should say what was chosen, what was rejected, the source, the reviewer, and the review date. This is what makes the skill evolving rather than a static list.
7. **Re-review on a cadence.** Culture changes. Re-check festival references, names in examples, and social terms at least annually or when a locale is added; feed corrections into `technical-documentation` as an owned doc.

## Context register shape

| Field | Why it matters |
|---|---|
| Reference | The name, festival, idiom, or social term |
| Region / language | Where it is meaningful |
| Use / avoid | The approved framing and the rejected framing |
| Source | Link or native reviewer evidence |
| Reviewer + date | Accountability and freshness |
| Next review | Prevents a living note from becoming folklore |

## Anti-patterns

- **One "Indian" persona for every locale.** It erases region, language, and community differences in one stroke.
- **Using a community as a punchline or shorthand.** It turns a user into a stereotype and damages trust across the ecosystem.
- **Literal festival/food translation.** An unrecognized reference does not illustrate anything.
- **Unsourced cultural claims in docs or model prompts.** They look authoritative and become wrong silently.
- **Treating a register as finished.** Without reviewer and date fields, the "living" register is just another stale doc.

Map to: `org-ethos` (cultural accuracy gate), `indic-multilingual-content`, `tamil-content-writing`, `technical-documentation`, `yazhi-review`.
