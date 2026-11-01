# Taste × Elegance

[Open the interactive guide and get the skill](https://michaeljabbour.github.io/amplifier-capability-taste-elegance/).

A lightweight skill that guides users and agents toward taste and elegance through the user's distinct experience and reasoning. Use it to explore writing, design, products, technical solutions, and agent-generated options, then choose a worthwhile refinement or reframe without overengineering. It does not give people taste or elegance, and an AI does not become the authority on either.

**Taste** is context-sensitive fit for an audience, purpose, and constraints. **Elegance** is a clear, economical resolution that accounts for users, maintainers, operators, and future work. Neither means luxury or minimalism. Evaluate artifacts and decisions, never a person's identity or inherent ability.

This project pairs the reusable [`improve-taste-and-elegance` skill](skills/improve-taste-and-elegance/SKILL.md) with an explanatory static website. The skill and [calibration reference](skills/improve-taste-and-elegance/references/calibration.md) began as the canonical revised source supplied for the existing [user-created skill](https://chatgpt.com/skills?skill_id=6ad24a616a5c8191932249aac4254289), including the user's clarification about facilitation, agency, and the choice between refinement and reframing. Version 0.2.0 adds Amplifier frontmatter and three clarifying sentences (delegation, where to save the decision note, and reference paths); the calibration reference is unchanged. The [2026-10-17 evaluation](docs/evaluations/benchmark-2026-10-17/REPORT.md) applies to its frozen snapshot. This project does not itself modify the installed skill.

## First use

Bring a draft, design or artifact and what matters to you about it. Compare it with a worse move and a better one, then choose with the reasons visible.

```sh
git clone https://github.com/michaeljabbour/amplifier-capability-taste-elegance.git
cd amplifier-capability-taste-elegance
python3 scripts/capability.py install --dest ~/.agents/skills
```

Requires Git and Python 3.11+. Use the skills directory supported by your agent. Ask for Taste × Elegance in a new session and supply one real task. The [install guide](docs/INSTALL.md) explains the complete ZIP alternative and safe updates.

## Use the skill

Give an agent the skill and a concrete artifact or set of options. Include the audience, purpose, constraints, and what success would look like. Share what shaped your choices: an experience, an admired or disliked example and why, a tension, what feels wrong, or a distinct intent that must survive changes. The agent should reflect your reasoning for correction and derive provisional criteria with you. This is a compact conversation, not a large questionnaire; at most three missing-context questions are appropriate, only where answers would change the recommendation.

If your tool supports reusable skills, copy the `skills/improve-taste-and-elegance/` directory (`SKILL.md` plus `references/`) according to that tool's instructions. Keep the relative `references/` path intact.

### In Amplifier

This repository is also an Amplifier bundle (`taste-elegance`). Add its behavior to your current host:

```bash
amplifier bundle add "git+https://github.com/michaeljabbour/amplifier-capability-taste-elegance@main#subdirectory=behaviors/taste-elegance.yaml" --app
```

For a local checkout that stays in step with your edits, use `file:///<path-to-checkout>/behaviors/taste-elegance.yaml` instead. Remove with `amplifier bundle remove taste-elegance-behavior --app`. Start a new session, then:

- **Skill:** `/improve-taste-and-elegance`, or ask for it by name. Nothing loads until it is used.
- **Mode:** `/taste` sets a working posture for a session: your lens first, one move at a time; every file edit asks you first, and shell or delegation warns once. `/mode off` leaves it.
- **Recipes:** staged runs that pause for your answers at each gate.
  - `@taste-elegance:recipes/taste-round.yaml` — one bounded round: reflect your lens, propose one change as a copy, then record a dated decision note. The artifact is edited only with `apply: "true"` and an approval message of exactly `adopt`; working copies and the decision note go in `.taste/` in your working directory.
  - `@taste-elegance:recipes/taste-spectrum.yaml` — a worked comparison of the original, a plausible worse version, and a proposed better one against the same brief. It never edits the artifact.

The skill is registered through `tool-skills`. If no other bundle in your host configures skill sources, Amplifier stops scanning its default skill directories (`.amplifier/skills` in the workspace and `~/.amplifier/skills`); add them to your own skills configuration if you need them. Don't also keep a hand-copied `improve-taste-and-elegance` in `~/.amplifier/skills`, or two copies will compete.

Example requests:

> Use improve-taste-and-elegance to explore this outage notice. My experience supporting anxious customers makes a direct next action important; I dislike notices that sound calm while hiding the impact. Reflect that intent, then propose one small improvement and how we could verify it. Keep this a critique.

> Help me explore these two onboarding flows against the same brief. Ask what shaped my judgment and reflect the important tension back to me. Check correctness, safety, accessibility, and feasibility before adoption. If a map helps, invite my self-placement, then offer a provisional view with evidence, confidence, and unknowns.

> Help me choose between delicately refining this authorized draft and making a meaningful conceptual jump. Preserve its warmth and specificity. In at most two rounds, preserve the baseline, predict benefit and regression risk, verify, and keep or undo the change. Stop when it meets the brief.

A useful response reflects your intent and provisional criteria, states assumptions and gates, offers independent coordinates with evidence and confidence when helpful, and proposes one next experiment with a tradeoff and stopping condition. You retain agency over the direction and preferences. See [a concrete proposal-only example](docs/EXAMPLES.md).

## How judgment works

Correctness, safety, accessibility, and feasibility are gates. Mark each **pass**, **fail**, **unknown**, or **not applicable**, with a reason. A failed critical gate blocks recommendation. An unknown critical gate is verification work, never an implicit pass. Repair the gate before polishing.

The map is a conversation aid, not an objective measurement, credential, or AI scoring authority. Prefer the user's self-placement and reasons, and use qualitative language by default. The [independent 1–5 anchors](skills/improve-taste-and-elegance/references/calibration.md) are optional when numbers help. Do not average the axes, add a combined score, use decimals, or imply universal rankings. Use a range or “unknown” when evidence is weak; name confidence and missing evidence for each axis. You can challenge the reading and revise the shared criteria.

The site's four quadrants are shorthand: right solution, beautifully resolved; right idea, awkward execution; polished answer, wrong problem; and rethink direction and execution. The selectable examples and before/after coordinates are **illustrative hypotheses, not measured data or completed assessments**. A real assessment needs a shared brief, gate checks, and evidence. Quadrants are not rigid scoring cutoffs.

## Improve without overengineering

Draw on the user's reasoning before asking for more context. Keep distinctive intent and contextual tensions visible instead of steering everyone toward the same aesthetic. Distinguish empirical checks—whether a task works or a requirement is met—from preferences grounded in the user's experiences and reasons.

Choose the bottleneck, then deliberately choose either a small hill climb or one meaningful conceptual jump, reframe, or structural alternative. A valuable reframe can be chosen before refinement stalls; a large redesign is not the default. Explain what must survive the change, predict its observable benefit and regression risk, preserve a baseline and rollback path, then verify before keeping it. Default to at most two rounds, including proposed but unverified rounds. Stop at worthwhile success or when the remaining gain does not justify its cost.

A critique authorizes recommendations. Edit only artifacts and scope the user authorized; it does not authorize external messages, publishing, or deployment. Never invent test results or user research. Coaching should use concrete decisions and offer one practicable growth action.

## Local development

The site follows the reference project's small Python static-builder approach: HTML, CSS, and JavaScript with no backend or runtime dependencies. Use Python 3.11 or later; no package installation is required.

From the project directory:

```sh
python3 scripts/build.py
python3 scripts/check.py
node --check site/site.js   # optional JavaScript syntax check; needs Node.js
python3 -m http.server 8000 --bind 127.0.0.1 --directory _site
```

Open <http://127.0.0.1:8000> in your browser. Stop the server with `Ctrl+C`. Re-run the build after source changes and reload the page. `_site/` is generated output. The website's copy and download actions serve this project's skill; preserve the calibration reference when installing it.

Preview over HTTP: the example selector reads a local JSON file. If clipboard access is unavailable, copy actions select the source and explain how to copy it manually. The skill bundle is a reproducible ZIP containing the project skill and calibration reference. The integrity check verifies local links and fragments, source fidelity, and ZIP contents. See [site details](site/README.md) and [validation evidence](docs/VALIDATION.md) for the implementation and browser checks.

The site opens with a one-minute lesson film that teaches the two questions with an everyday example; see [how it was made](docs/FILM.md).

The public source is in the [amplifier-capability-taste-elegance repository](https://github.com/michaeljabbour/amplifier-capability-taste-elegance). The primary entry point is the [live website](https://michaeljabbour.github.io/amplifier-capability-taste-elegance/). The Pages workflow builds and checks `_site/` on pushes to `main`, then publishes only that static output. It uses GitHub’s official actions pinned to fixed commits and needs no project secrets. See [site details](site/README.md) for deployment maintenance.

## Project contents

- `skills/improve-taste-and-elegance/SKILL.md` — canonical revised instructions for facilitation, agency, jumps, and refinements.
- `skills/improve-taste-and-elegance/references/calibration.md` — eight invitations, two ways forward, optional independent anchors, and examples.
- `skills/improve-taste-and-elegance/references/delegated-loop.md` — rounds run without the user: the lens captured once, a bounded budget, fixed-condition before/after captures, and one review together.
- `bundle.md`, `behaviors/taste-elegance.yaml` — the Amplifier bundle and its installable behavior.
- `modes/taste.md` — the `/taste` mode.
- `recipes/` — the `taste-round` and `taste-spectrum` staged recipes.
- `docs/EXAMPLES.md` — a worked, explicitly proposal-only assessment.
- `scripts/build.py` — dependency-free static build entry point.
- `scripts/check.py` — local link, source, and download integrity checks.
- `site/` — page template, metadata, styles, local assets, and interaction code.
- `_site/` — generated website and downloadable skill assets.

## Limits

This is a structured aid to developing and expressing judgment, not a validated psychometric instrument, objective quality metric, or substitute for domain expertise. Anchors depend on the brief, the user's intent, and available evidence; two careful reviewers may disagree. They cannot establish a person's talent or general competence. An agent can help articulate reasons and test consequences, but cannot confer taste or settle a preference by assigning a number.

The graph cannot assess an uploaded artifact, certify correctness or accessibility, or demonstrate causal improvement. Its examples are invented for explanation. Actual tests, inspection, and user research must be identified separately; unknowns remain unknown until verified. Essential complexity sometimes cannot be removed. A good outcome may stay below 5 on either axis because the user's priorities and costs govern.

## License and provenance

MIT; see [LICENSE](LICENSE). The preserved family-theme snapshot has its own
[MIT notice](site/theme/LICENSE). The page follows Decisioncraft's local static site
as a design and implementation reference. Its product text, media, repository
configuration, and institutional attribution are not part of this project.


## Portable capability and ownership

Make it more intentional and simpler while keeping it yours.

Read the [installation guide](docs/INSTALL.md) for the supported local path and [consolidation record](docs/CONSOLIDATION.md) for ownership and evidence limits. Canonical catalog name: **Taste × Elegance**; repository: `amplifier-capability-taste-elegance`.

## Repository migration

This repository was renamed from `amplifier-skill-taste` to `amplifier-capability-taste-elegance`. Existing installed method names, bundle aliases and native interfaces stay the same. See the [migration guide](https://michaeljabbour.github.io/migration/) and [repository map](https://michaeljabbour.github.io/migration/mapping.json) for source URL updates.

## Structured record compatibility

The optional improvement record now has an explicit delegated **v2** contract. The closed [v1 schema](skills/improve-taste-and-elegance/references/improvement-round.schema.json) remains byte-identical; new loop/lens/capture metadata uses [v2](skills/improve-taste-and-elegance/references/improvement-round.v2.schema.json). Keep v1 output for v1-only consumers. Do not strip evidence or relabel versions to bypass validation. [Record guidance](skills/improve-taste-and-elegance/references/improvement-round.md) explains the independent two-round budget, scope and proposed/no-authority default.

For deterministic contract regressions, use an existing environment with `jsonschema`: `make contract-check PYTHON=/path/to/python`. This runs schema and semantic boundary fixtures without installing packages, calling models or measuring aesthetic or human benefit. The optional checker returns no runtime authority.
