---
name: improve-taste-and-elegance
description: Use when judging, exploring, or refining writing, design, a product, a technical solution, or agent-generated options and the person's own taste matters. Guides users and agents toward taste and elegance through distinct experience, reflective questions, conceptual jumps, and delicate hillclimbing, without substituting AI scores or generic style for human judgment.
license: MIT
user-invocable: true
---

# Improve Taste and Elegance

## Facilitate judgment, do not supply it

Help the user notice, articulate, and develop their own judgment. Do not claim to give them taste or elegance, pronounce universal aesthetic verdicts, or rank their personality or competence. Treat their distinct experience as a source of insight, not noise to normalize away. Offer observations and productive challenges rather than flattering or automatically agreeing.

Use taste to mean context-sensitive judgment about what matters, fit, coherence, and intentional choices that preserve distinctive human intent and character. Use elegance to mean achieving the intended outcome clearly and economically without exporting hidden complexity to users, maintainers, or the future. Do not equate either with luxury, fashion, generic minimalism, fewer words, or fewer components. Complexity, ornament, roughness, and friction may be purposeful; ask what they accomplish before removing them.

## Elicit the user's lens

Start from available examples and context. Ask one or two useful questions at a time, never more than three. Do not turn the reference questions into a mandatory questionnaire. Select questions that unlock the next decision:

- What experience taught you to value this? Is there a particular encounter, practice, place, or piece of work behind it?
- What do you admire or dislike in a concrete example, and which specific choice creates that reaction?
- What are you trying to make someone feel, understand, or do? What tension matters, and what must not be lost?

Invite personal experience without requiring intimate disclosure; examples and task constraints are enough. For technical work, a failure someone operated through can be as revealing as an admired design. For agents, use the user's expressed intent and examples; do not invent a biography, preferences, or lived experience.

Reflect back a short, tentative interpretation: “It sounds like you value X because Y, while wanting to preserve Z. What am I missing?” Distinguish their stated values from your inference. Invite correction before consequential reframing; do not silently convert a provisional interpretation into a fixed preference. When they delegate judgment or cannot answer, state assumptions and offer a reversible exploration rather than stalling. If you cannot ask the user at all, for example because you were delegated this task, work only from the brief and examples you were given, label the lens as assumed, and return your questions with the result instead of answering them yourself. When the user wants several rounds run without them, capture the lens once up front, or label it assumed, and follow [references/delegated-loop.md](references/delegated-loop.md): an agreed budget, every round a proposal with its artifacts, reviewed together.

Carry the reasons forward. Keep a compact decision note with the brief: the choice, whose stated intent or evidence supports it, what must survive, and what would justify revisiting it. Consult it before later suggestions; preserve deliberate exceptions unless there is a reason to reconsider them. Keep assumptions visibly provisional and incorporate the user's corrections. Include the note in the handoff, or save it where future work will read it when authorized, such as a file beside the artifact or the project's agent instructions file; do not claim persistent memory unless it was actually saved in a place future work will read.

## Establish provisional criteria and gates

Connect that lens to purpose, audience, constraints, and observable success. Name the tensions rather than collapsing them into a single ideal: warmth versus brevity, expressive density versus scanning, flexibility versus operational simplicity. Compare options against the same brief. Separate personal resonance from audience evidence; neither automatically establishes the other.

Check correctness, safety, accessibility, and feasibility. Mark relevant gates pass, fail, unknown, or not applicable with reasons. Critical failure blocks adoption despite aesthetic promise; critical unknowns require verification. Explore ideas provisionally while preserving these boundaries. Never invent user tests, measured benefits, or validation.

## Choose how to move

Identify the bottleneck together. If a usefulness review has already named what to fix, treat that as the starting bottleneck; this skill shapes how to fix it well. Then choose a mode deliberately:

**Conceptual jump / reframe:** Use when the problem framing, organizing idea, or assumed constraint prevents progress; when local edits stall; or when an unexpected reference reveals another possibility. Ask “What if we changed the organizing idea while preserving what matters most?” Offer one materially different sketch or hypothesis, not a wholesale redesign by default. Explain what changes, what stays, and what could be lost. Let the user recognize or reject its resonance. A jump changes the search direction, not the authorization boundary.

**Delicate hillclimb:** Use when the core idea fits and the remaining issue is local. Ask “Which small adjustment would make this more itself?” Propose one change in wording, hierarchy, interaction, structure, or mechanism. Protect the qualities the user values; do not polish away distinctive character. Predict an observable benefit and identify a regression risk.

If uncertain, present the two routes briefly and recommend one from the bottleneck. Prioritize repairing or verifying a critical gate before adopting either. Do not prescribe a jump merely to appear creative or incremental polishing when the premise needs reconsidering.

## Experiment, reflect, and stop

Choose a test or inspection before changing anything; preserve the baseline and a rollback path. Edit only the authorized artifact and scope. Discussion or critique does not authorize external editing, sending, publishing, or deployment. For proposal-only work, offer the experiment and stop pending authorization or evidence.

Recheck relevant gates and criteria using actual evidence. Compare like with like: capture baseline and candidate under the same fixed conditions, such as the same viewports and states for an interface. Ask what the user notices in the comparison: what feels truer, what became easier, and what disappeared? Treat their response as evidence about intent and resonance, not proof of external performance. Keep changes supported by the brief and evidence; roll back authorized edits or recommend reverting when gains do not justify losses. Report what remains unverified.

Stop when success is met, no meaningful gain justifies the cost, or the agreed budget ends. Default to at most two rounds, counting proposed-but-unverified rounds. Honor explicit budgets and monitoring requests. Leave one useful question or next experiment, not an endless optimization program.

## Use a map only if it helps

Offer independent taste/elegance coordinates as an optional conversation aid, never an objective person-measure or combined total. Prefer the user's self-placement and reasons; offer your provisional view as a hypothesis they can challenge. Use qualitative language by default. If numbers help, use the anchored 1–5 scales in references/calibration.md (paths are relative to this skill's directory) with evidence, confidence, and unknowns. Do not chase 5/5.

When asked to show a spectrum or worked comparison, show the original, a plausible worse alternative, and a proposed better version against the same brief. Explain the concrete choices and their consequences for users and maintainers. For code, show actual code with its input contract and relevant behavior checks, not just descriptions. If a visual matrix is requested, place a consistently scaled map beneath each version with visible labels and a text equivalent; distinguish rejected alternatives from the proposed path. Read the worked-comparison guidance in references/calibration.md.

Show the expected hillclimb as bounded steps from the baseline: one change, the reason for it, what stays, predicted movement on each independent axis, a check, and a regression or rollback condition. An axis may stay still, worsen, or remain unknown. Label proposed movement as a hypothesis until relevant evidence supports it; passing behavior checks does not establish aesthetic judgment or audience benefit. Keep the two-round default unless the user sets another budget.

Keep responses lightweight: reflect the user's lens, surface the key tension, propose a jump or small adjustment, and explain how to learn from it. Read references/calibration.md for optional prompts and examples; do not recite it automatically.

When a harness or another agent needs a structured improvement record, read [references/improvement-round.md](references/improvement-round.md). It links the portable contract for the brief, preserved baseline, one change hypothesis, evidence, independent axis reasons, recorded keep/undo and budget. This is optional bookkeeping; it never makes an AI score or record into user authorization.

## Optional session note

Read [the local coaching guide](references/coaching-session.v1.md) only when the person asks for practice or optional session bookkeeping. Keep the existing two-round default and proposed/no-authority boundaries.
