---
name: tone-of-voice-application
description: Use when writing or reviewing any social media copy that must match a specific brand voice — captions, posts, reel scripts, or repurposed content. Applies a brand's tone rules consistently and flags when no brand voice reference is available.
---

This skill takes any draft social copy and applies a supplied brand tone-of-voice reference to it, or applies safe default voice rules when no brand reference exists. It ensures consistency across platforms and guarantees that the team is explicitly aware of which voice rules were applied to the final output.

## Step 1 — Check for a brand voice reference

Look for a tone-of-voice doc, style guide, or explicit voice instructions in the request or repo. If found, extract the following:

| Reference Element | What to look for and extract |
|---|---|
| Personality traits | Tone boundaries (e.g. "witty but not sarcastic", "authoritative but warm") |
| Vocabulary | Banned words, preferred terms, industry jargon rules |
| Emoji policy | Frequency (never / sparingly / frequently) and specific approved/banned emojis |
| Structure | Sentence length, formality preference, reading level |
| Examples | Representative posts that model the voice well |

## Step 2 — No reference found? Use defaults, and say so

Default voice rules:
1. Conversational and confident, never robotic or corporate
2. Active voice, short sentences, one idea per line
3. Emoji sparing — only where it adds clarity or warmth
4. Avoid jargon unless the audience is explicitly technical

Always state in output: `VOICE SOURCE: default rules (no brand reference found)`.

## Step 3 — Apply and self-check

Before returning copy, check it against these points:
- Does every sentence sound like it could be said out loud, not read off a slide?
- Any banned words or off-brand jargon snuck in?
- Is emoji usage matching the stated policy exactly (not just "seems fine")?
- Would this line stand out as generic AI copy? If yes, rewrite it.

## Common failure modes

- **Voice drift across long content**: applying the voice correctly in the first paragraph but slipping into generic tone by the end. Breaks consistency across multi-post repurposing — re-check the last third of any output against the voice rules, not just the opening.
- **Treating "playful" as "unprofessional"**: brand tones like "playful" or "witty" get miswritten as sloppy or sarcastic, which can misrepresent the brand publicly and needs manual review before those tones are trusted.
- **Silent default fallback**: applying default voice rules without flagging it, so the team publishes generic-sounding copy assuming it was brand-matched. Always state the voice source in output.
- **Copying example posts too closely**: using supplied example posts as templates that get reworded rather than as a style reference, producing repetitive-sounding content across campaigns.
