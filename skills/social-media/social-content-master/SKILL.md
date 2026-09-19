---
name: social-content-master
description: Use when a request asks to create, draft, rewrite, or repurpose content for social media — posts, captions, reel/short-form video scripts, or turning one long-form asset into multiple platform posts. Orchestrates the social-media skill set (tone, captions, reel scripts, repurposing, hashtags) into one end-to-end content generation workflow.
---

This orchestrator skill routes a content request through the right combination of the social-media skill set below, in order, rather than duplicating their logic here. It acts as the entry point for all end-to-end content generation workflows.

## Skill set this orchestrates

| Skill | Called when |
|---|---|
| `tone-of-voice-application` | Always — applied to every piece of copy before it's finalized |
| `social-caption-writing` | Request is a post/caption (Instagram, LinkedIn, X, Facebook) |
| `reel-script-generation` | Request is a reel, short, or TikTok script |
| `content-repurposing` | Source material (blog, transcript, doc) is provided instead of a bare topic |
| `tamil-social-content` | Request asks for Tamil copy, or a Tamil version alongside English |
| `content-quality-review` | Always — run once across the full batch, after tone is applied and before hashtags |
| `hashtag-and-platform-strategy` | Always — applied last, after copy/script is finalized and quality-reviewed |

## Step 1 — Get the brief

Required before routing to any sub-skill:
1. **Topic or source material** — idea, bullet points, doc, or transcript
2. **Platform(s)** — Instagram / LinkedIn / X / YouTube Shorts / TikTok / Facebook
3. **Format** — single post, carousel, reel/short script, or thread
4. **Goal** — awareness, engagement, conversion, education, or announcement
5. **Language** — English by default; note if Tamil (script or Tanglish) is needed, alongside or instead of English
6. **Brand tone-of-voice reference** — if none supplied, `tone-of-voice-application` falls back to its own defaults

If 1–4 are missing and can't be reasonably inferred, ask one combined clarifying question rather than routing blind.

## Step 2 — Route the request

1. If **source material** was provided (not just a bare topic) → run `content-repurposing` first to extract insights and assign each to a platform/format
2. For each resulting platform/format pair:
   - If format is a **reel/short/TikTok** → run `reel-script-generation`
   - Otherwise → run `social-caption-writing`
3. Run `tone-of-voice-application` on every piece of copy or script produced, regardless of path taken
4. If Tamil output was requested → run `tamil-social-content` on the finished, tone-approved English draft to produce the Tamil adaptation
5. Run `content-quality-review` once across the ENTIRE batch of pieces produced in this request — never one piece at a time — to catch cross-platform repetition, generic phrasing, and weak hooks
6. Run `hashtag-and-platform-strategy` last, on the finished, quality-reviewed copy, to attach hashtags and posting notes

## Step 3 — Assemble final output

Combine each sub-skill's output into one response block per platform:

```text
PLATFORM: <name>
FORMAT: <post / carousel / reel script>
VOICE SOURCE: <brand ToV doc name> OR "default voice rules used"
QUALITY CHECK: <"passed as-is" OR what was changed and why>
---
<copy or script here>
---
HASHTAGS: #tag1 #tag2 #tag3
NOTES: <notes from hashtag-and-platform-strategy, plus any flags raised by other skills>
```

If multiple platforms were requested or produced via repurposing, repeat this block once per platform — never merge platforms into one block.

## Common failure modes

- **Skipping tone-of-voice on repurposed content**: applying `tone-of-voice-application` only to freshly-drafted copy and forgetting it on outputs that came from `content-repurposing`, leaving repurposed posts off-brand.
- **Routing a request to the wrong sub-skill**: sending a reel request through `social-caption-writing` (or vice versa) because the format wasn't confirmed in Step 1, producing output in the wrong shape entirely.
- **Running hashtag strategy before copy is final**: attaching hashtags before the caption/script is finished, so hashtags don't match a since-edited final draft.
- **Silent routing with no brief**: guessing platform, format, or goal instead of asking the one combined clarifying question, producing output the requester didn't actually ask for.
