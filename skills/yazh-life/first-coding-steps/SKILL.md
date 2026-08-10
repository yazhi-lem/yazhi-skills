---
name: first-coding-steps
description: Use when a ~12-year-old is learning to program — first Python or Scratch project, a school computing assignment, a game they want to build, or an error message they can't read. Helps you keep them building things they care about and teach them to debug, instead of drowning them in syntax rules or handing over working code they don't understand.
---

Kids quit programming for two reasons: the first project was a temperature converter nobody wanted, or the first red error message felt like a verdict on them. Neither is about intelligence. Pick projects with a visible result and teach error messages as ordinary instructions, and a 12-year-old will out-persist most adults.

## Choosing the first projects

| Week | Project | Teaches | Visible result |
|---|---|---|---|
| 1 | Number-guessing game | input, loop, if/else | Computer "plays" with them |
| 2 | Quiz on a topic they like | lists, score counter | Their friends can play it |
| 3 | Dice/coin simulator, 1000 rolls | random, counting, simple stats | A surprising real answer |
| 4 | Turtle or p5 drawing | loops, coordinates, functions | A picture on screen |
| 5-6 | Something *they* proposed | everything, plus debugging | The reason they keep going |

Anything with no visible output — sorting a hardcoded list, converting units — belongs in week 8, not week 1.

## Workflow

1. **Ask what they want to make before teaching any syntax.** A game, a bot for their group chat, a score tracker for their team. Teach exactly the syntax that project needs, when it needs it.
2. **Get a running program on screen in the first 10 minutes.** `print("hello")` executing beats an hour of setup. If the environment fights back, move to an in-browser editor and fix tooling later.
3. **Teach the read-the-error ritual as step one, every time:** last line first (the error type and message), then the line number, then look one line *above* it too. Most 12-year-olds never read the message at all; this single habit is worth more than any syntax lesson.
4. **Change one thing, then run.** Not five things. When something breaks after one change, the cause is known. This is the whole discipline of debugging, and it's learnable at 12.
5. **Coach, don't paste.** Follow the hint ladder in `homework-coaching`: point at the region, name the concept, show a parallel example — full code only as a last resort, and then have them retype it and explain each line.
6. **Teach `print()` debugging early.** Print the variable right before the line that breaks. Seeing that `score` is the text `"5"` and not the number `5` explains more than any lecture about types.
7. **Save and name versions.** A folder with `game_v1.py`, `game_v2.py` before every big change — the 12-year-old version of source control, and it prevents the "I broke it and can't get back" quit moment.
8. **Set the safety rules once:** no real name, school, address, or photos in code or usernames; never paste a password into a program or a website; ask before installing anything. See `online-safety`.

## Anti-patterns / common failure modes

- **Syntax-first teaching.** Six lessons on variables, types, and operators before anything runs — the kid concludes programming is boring homework and they're right.
- **Pasting corrected code.** It works, they learn nothing, and the next bug is just as impossible as this one.
- **"Just Google it."** A 12-year-old doesn't yet know which words of the error are the searchable part; show them how to strip the filename and their variable names out of the query.
- **Treating errors as failure.** Every professional's day is full of them; if red text feels like a mark against them, they'll stop trying things.
- **Environment yak-shaving on day one.** An hour of PATH problems before any code runs ends more coding careers than any hard concept.

For the tutoring stance see `homework-coaching`; for pitching explanations right see `age-appropriate-explaining`; for account and privacy rules see `online-safety`.
