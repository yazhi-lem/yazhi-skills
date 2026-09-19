# Using the Social Media Content Pipeline

## What this is
A set of skills in our `yazhi-skills` repo that generates ready-to-post social media content — captions, LinkedIn posts, reel scripts — in our actual brand voice, with Tamil support if needed.

## How to use it
Just ask for what you need in plain language, starting with the name of the master skill:

```
Using social-content-master, write a [PLATFORM] post about [TOPIC], goal: [awareness/engagement/conversion/education/announcement]
```

**Examples:**
- "Using social-content-master, write an Instagram post about our new product launch, goal: awareness"
- "Using social-content-master, write a LinkedIn post and a Reel script about our Q3 results, goal: engagement"
- "Using social-content-master, write this in Tamil and English for Instagram, about [topic]"

You don't need to know anything about how it works internally — just describe what you need the way you'd ask a colleague.

## What you'll get back
Each platform's post will come formatted like this:

```
PLATFORM: <name>
VOICE SOURCE: brand-voice-reference.md
QUALITY CHECK: <passed, or what was changed>
---
<the actual post/script>
---
HASHTAGS: #tag1 #tag2
NOTES: <formatting or posting tips>
```

## What to check before posting
- Does it sound like something we'd actually say? (Bold, direct, no fluff, no emoji)
- Does the QUALITY CHECK line say anything was flagged or changed? If so, that's worth a quick read.
- Hashtags and notes are separate from the copy — edit them freely.

## If something feels off
Just say so directly: "this sounds too generic" or "this hashtag doesn't fit" — you can ask for a rewrite the same way you'd give feedback to a person. Please flag anything that feels wrong so we can improve it — this is the first real test of the pipeline outside of internal testing.

## Try this first
Pick one real post you were already planning to write this week — not a test topic — and run it through. That's the most useful thing you can do right now.
