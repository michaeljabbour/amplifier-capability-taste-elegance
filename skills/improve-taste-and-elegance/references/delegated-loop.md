# Delegated rounds

Use this when the user wants several rounds run without them, for example an agent refining something it built while the person reviews later. The rest of the skill still holds. Rounds produce proposals and evidence; the user's judgment and authorization stay with the user.

## Capture the lens once

Before the first round, ask for a short brief. Choose at most three questions, for example:

1. What example, or what experience, shaped what you value here?
2. What must survive any change?
3. What would make you say a round was worth keeping, and when should the loop stop?

Also agree the logistics plainly: the artifact and scope the rounds may touch, where candidates live (a copy or branch, never the original unless authorized), the round budget, and what the user wants to review.

Record their answers as the stated lens, in their words. If they cannot answer, build an assumed lens from the brief and examples only, label it assumed in every round, and put your questions at the top of the review. Do not invent a biography or preferences. Under an assumed lens, prefer delicate hillclimbs; offer a conceptual jump as a separate, unstacked proposal, since it changes direction on a lens no one has confirmed.

## Run bounded rounds

- Honor the agreed budget. Without one, the default of two rounds holds. Every round counts, including unverified ones.
- One change per round, with its hypothesis, predicted benefit, regression risk, gates and rollback.
- Each round is a proposal. Building the next round on a candidate is not adoption. Record the decision as proposed with no authority, unless the user delegated keeps explicitly in the brief; cite that delegation, and their review can still undo it.
- Prefer rounds from the same baseline when changes are separable. When a round builds on an earlier candidate, name that round so the user can undo from the earliest one they reject.
- A critical gate that fails or stays unknown stops that line of rounds.
- Stop early when a round shows no meaningful gain. Do not spend the budget to fill the review.
- Keep axis movements as hypotheses. Your reading of the comparison is not the user's taste.

## Compare under fixed conditions

A round is comparable only when baseline and candidate are captured the same way. Choose the conditions before the first round and keep them for the loop.

- **Interfaces:** the same viewports (at least one narrow phone width and one desktop width), the same states (empty, loading, populated, error, and any state the change touches), the same data, theme, zoom and input method. Capture baseline and candidate with the same tool. Add a state if a round needs it, and capture it for the baseline too.
- **Writing:** the same excerpt, rendered where the reader will meet it, and the same surrounding context.
- **Slides, images, video, audio:** the same display size or playback setup, the same frames or timestamps, side by side.
- **Code and mechanisms:** the same inputs, commands and checks, with output kept.

Artifacts show what changed. They are evidence for gates and for the user's comparison, not proof of taste or audience benefit. Accessibility checks such as contrast, keyboard paths and text size are gates; record them as gates.

## Hand over the rounds together

Give the user one review: the lens and whether it is stated or assumed, then per round the before/after artifacts in the same order, the change, gates, axis reasons, dependencies and the undo. End with your questions, most decisive first, and one suggestion for what to try next. Ask them to keep or undo each round and to correct the lens. Their reactions update the decision note and the lens for any later loop.

When a harness needs records, write one improvement-round record per round ([improvement-round.md](improvement-round.md)). Use `loop` to group the rounds and name stacked parents, `brief.lens_ref` to point at the lens, and `comparison.captures` for the fixed-condition artifacts.

## Pairing

When a usefulness review has already named what to fix, for example a criterion that blocks a stranger, take that as the bottleneck. That review decides what to improve; this skill decides how to improve it while keeping what makes the work itself. Do not quietly widen the scope to polish elsewhere.
