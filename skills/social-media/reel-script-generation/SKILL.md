---
name: reel-script-generation
description: Use when scripting a short-form video for Instagram Reels, YouTube Shorts, or TikTok from a topic or brief. Produces a timestamped script with visual cues, on-screen text, and a hook designed to work with sound off.
---

This skill converts a topic or brief into a structured short-form video script that a video editor or presenter can shoot from directly. It ensures timing, visual cues, and on-screen text are spelled out clearly for production.

## Step 1 — Confirm inputs

Required: topic, target length (typically 15–60 sec), and goal (education, announcement, entertainment, conversion). If a specific length isn't given, default to 20–30 seconds.

## Step 2 — Structure

| Segment | Timing (20–30 sec video) | Purpose |
|---|---|---|
| Hook | 0:00–0:03 | Visual + on-screen text hook; must land with sound off |
| Body beats | 0:03–end minus 5 sec | 2–4 fast beats, each with a visual cue and a line of on-screen text / VO |
| CTA | Final 3–5 sec | One action, reinforced with on-screen text |

## Step 3 — Output format

```text
[0:00–0:03] HOOK
Visual: <what's on screen>
Text/VO: "<line>"

[0:03–0:15] BEAT 1
Visual: <cue>
Text/VO: "<line>"

[repeat BEAT rows as needed]

[final 3–5s] CTA
Visual: <cue>
Text/VO: "<line>"
```

## Step 4 — Self-check before returning

1. Does the hook make sense with the sound off, using only the visual + on-screen text?
2. Is each beat short enough to hold attention (roughly 3–5 sec per beat)?
3. Is there exactly one CTA, not several competing asks?

## Common failure modes

- **Sound-dependent hooks**: writing a hook that only works if the viewer has audio on, which fails on platforms where most views start muted. Always pair the hook line with an on-screen text equivalent.
- **Overloaded beats**: cramming two ideas into one beat, making the pacing feel rushed and hurting watch-through rate. Split into two beats instead.
- **Missing visual cues**: writing only the spoken/on-screen line without specifying what's happening visually, leaving the editor to guess and causing rework.
- **CTA buried mid-script**: placing the call to action before the final beats instead of at the very end, which lowers completion-to-action rate since viewers who drop off early never see it.
