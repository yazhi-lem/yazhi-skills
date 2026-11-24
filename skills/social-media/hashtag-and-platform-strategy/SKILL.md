---
name: hashtag-and-platform-strategy
description: Use when finalizing hashtags, posting-time notes, or platform formatting guidance for a social media post, caption, or reel script that has already been drafted. Helps you attach platform-specific metadata without padding tags, claiming live trends you never checked, or overriding the finished copy.
---

This skill adds the final layer of platform-specific metadata — hashtags and posting notes — to already-drafted copy. It keeps this metadata separate from the caption itself so the social team can adjust it independently before publishing. Run it last, after `content-quality-review` has passed the batch and the copy will no longer change.

## Workflow

1. **Confirm the copy is final.** If a draft is still being edited, stop and return it to `social-content-master` — hashtags chosen for one draft often no longer match a rewritten hook.
2. **Pick hashtag count and mix per platform** from the table below. These are starting ranges, not quotas: fewer relevant tags beat padded ones.
3. **Check every tag against the actual content.** A tag earns its place only if the post says something about that topic. If fewer relevant tags exist than the target count, ship fewer and note why.
4. **Flag the trend caveat explicitly.** Suggestions here are pattern-based on the topic, not pulled from live trend data. State that in the output so the team can verify against current trends before publishing.
5. **Add posting notes only when they change a decision** — format constraints, a genuinely platform-specific quirk, or a timing starting point. Do not restate the caption or pad the notes section.
6. **Emit the fixed output shape** and keep hashtags/notes separate from the copy, so a publisher can edit either field without touching the other.

| Platform | Count | Mix |
|---|---|---|
| Instagram | 3–8 | Broad + niche |
| X / Twitter | 0–2 | Only if genuinely trending/relevant |
| LinkedIn | 3–5 | Industry/professional |
| TikTok / Shorts | 3–5 | 1 trending + rest niche |
| Facebook | 0–2 | Optional, low impact on this platform |

## Posting notes: what qualifies

- **Format reminders** — e.g. "square or 4:5 crop for Instagram feed", when the asset is not already sized correctly.
- **Timing windows** — framed as a starting hypothesis from general audience patterns, never as a measured fact about this account. The account's own analytics are the only authoritative source.
- **Platform quirks** — e.g. X's weak response to hashtag-heavy posts, or a link preview that needs checking, when they apply to this specific post.

If none of these change the publishing decision, write `NOTES: none` rather than inventing a remark.

## Output format

```text
HASHTAGS: #tag1 #tag2 #tag3
NOTES: <format, timing, or platform-quirk notes>
```

## Common failure modes

- **Padding hashtag counts**: adding loosely-related or generic tags just to hit a target number, which can reduce reach quality rather than improve it.
- **Treating hashtag suggestions as verified trends**: presenting pattern-based guesses as if they were confirmed trending tags, when no live data source was checked.
- **One hashtag set for all platforms**: reusing the same tags on X and Instagram, ignoring that X performs worse with multiple hashtags while Instagram rewards a broader mix.
- **Posting-time overconfidence**: stating a specific "best time to post" as fact rather than a general starting point, when actual best time depends on the specific audience's activity data.
- **Rewriting copy to fit tags**: changing a final, quality-approved hook so a hashtag fits — the metadata exists to serve the copy, not the other way round.

For the workflow that leads here see `social-content-master`; for the quality gate immediately before this step see `content-quality-review`; for Tamil hashtags and script-specific formatting see `tamil-social-content`.
