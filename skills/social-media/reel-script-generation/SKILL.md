---
name: reel-script-generation
description: Use when scripting a short-form video for Instagram Reels, YouTube Shorts, or TikTok from a topic or brief. Produces a timestamped script with visual cues, on-screen text, and a hook designed to work with sound off. Helps you keep beats short and the call to action at the end.
---

This skill converts a topic or brief into a structured short-form video script that a video editor or presenter can shoot from directly. It ensures timing, visual cues, and on-screen text are spelled out clearly for production. The output is a shootable script, not a paragraph of ideas — every segment has a time range, a visual, and a line.

## Workflow

1. **Confirm inputs** — topic, target length, and goal (education, announcement, entertainment, conversion). Default to 20–30 seconds when no length is given; accept 15–60 seconds as the normal range, and ask one combined question if the goal is genuinely unclear.
2. **Draft the hook first**, as a visual plus an on-screen line that makes sense with the sound off. Most feeds start muted; a voice-only hook loses the first three seconds.
3. **Break the body into 2–4 beats**, one idea per beat, roughly 3–5 seconds each. Give every beat a distinct visual cue and one line of on-screen text or voiceover — never two ideas in one beat.
4. **Place one CTA in the final 3–5 seconds.** Choose a single action (follow, comment, read the link) and repeat it in on-screen text. Competing asks split attention and convert worse than one clear ask.
5. **Time the whole script** against the segment table below. If the segments exceed the requested length, cut a beat — do not speed up delivery or shrink the hook/CTA below their floors.
6. **Self-check before returning** — run the four questions in the checklist and fix any failure rather than flagging it in the handoff.

| Segment | Timing (20–30 sec video) | Purpose |
|---|---|---|
| Hook | 0:00–0:03 | Visual + on-screen text hook; must land with sound off |
| Body beats | 0:03–end minus 5 sec | 2–4 fast beats, each with a visual cue and a line of on-screen text / VO |
| CTA | Final 3–5 sec | One action, reinforced with on-screen text |

## Self-check

1. Does the hook make sense with the sound off, using only the visual + on-screen text?
2. Is each beat short enough to hold attention (roughly 3–5 sec per beat)?
3. Is there exactly one CTA, not several competing asks?
4. Can an editor shoot this without guessing — does every segment name a visual and a line?

## Output format

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

Attach hashtags and posting notes only after the script is final, using `hashtag-and-platform-strategy`; run `content-quality-review` across the batch first. For Tamil scripts use `tamil-social-content` to adapt the on-screen lines.

## Common failure modes

- **Sound-dependent hooks**: writing a hook that only works if the viewer has audio on, which fails on platforms where most views start muted. Always pair the hook line with an on-screen text equivalent.
- **Overloaded beats**: cramming two ideas into one beat, making the pacing feel rushed and hurting watch-through rate. Split into two beats instead.
- **Missing visual cues**: writing only the spoken/on-screen line without specifying what's happening visually, leaving the editor to guess and causing rework.
- **CTA buried mid-script**: placing the call to action before the final beats instead of at the very end, which lowers completion-to-action rate since viewers who drop off early never see it.
- **Timing drift**: assigning generous beat lengths that push a "30-second" script to 45 seconds — total the segments before handing off, then cut a beat rather than rushing delivery.
