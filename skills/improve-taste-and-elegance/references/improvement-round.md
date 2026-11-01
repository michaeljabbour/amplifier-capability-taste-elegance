# Improvement round records

Taste owns this optional comparison contract. A record keeps the brief, immutable baseline, one hypothesis, gate evidence, separate taste/elegance reasons and a budget visible. It does not require a harness to apply the skill and never turns bookkeeping into authorization.

## Select an explicit version

- [improvement-round/v1](improvement-round.schema.json) is the unchanged, closed contract for existing consumers. Its identifier and allowed fields are frozen. A v1 record cannot contain the new delegated fields.
- [improvement-round/v2](improvement-round.v2.schema.json) explicitly adds `loop`, `brief.lens_ref` and `comparison.captures`. Each capture names its condition, method and paired artifacts. Use it for [delegated rounds](delegated-loop.md) only when the consumer supports v2.

A closed v1 validator rejects new properties even when a newer writer calls them optional. Do not silently send a v2 record to a v1 consumer, strip evidence to downgrade it, or relabel its schema version. Existing v1 writers and the old contract pointer remain valid. A version change is not permission to change the method or rerun historical evaluations.

## Preserve the method and boundaries

Preserve the brief and baseline before one authorized change. Predict benefit and regression risk, then compare under the same brief and fixed conditions. Either axis can stay unknown or worsen. Technical checks do not establish aesthetic improvement, reader benefit or human adoption.

A critical failed or unknown gate blocks a keep. In a delegated line it also stops continuation. Every round counts against the agreed budget, including proposed and unverified rounds. The default budget stays two; a larger limit must come from the operator's actual brief, not from a record claiming more rounds.

The normal v2 decision is explicitly `action: proposed`, `authority: none`. Both fields are required; JSON Schema defaults are annotations and do not fill missing values. `defer` also carries no authority. A keep or undo requires the user's actual decision or an explicit delegation. Records cite that source and rollback, but cannot authenticate it or grant runtime permissions.

## Optional read-only verification

The [checker](validate_round.py) loads only these package-owned schemas, checks structural and cross-record consistency, and never reads artifact references, edits files, calls a provider or executes a decision. It requires an already available Python environment with `jsonschema`; it installs nothing. The skill itself has no new execution dependency.

Supply operator context independently from model-produced records. It names `artifact_refs` permitted for baseline/candidate, rollback and captures, `max_rounds` (default two), any matching `decision_authorizations`, and optional `stated_lens_refs` for an actual correction. Do not derive this context from the candidate record. Even a successful match only establishes metadata consistency; the host must still enforce its real authorization and scope.

```sh
python3 references/validate_round.py round.json --context operator-context.json --previous earlier-round.json
```

Omit `--previous` for the first round. Example context for two proposal rounds:

```json
{
  "max_rounds": 2,
  "artifact_refs": ["baseline.md", "candidate-one.md", "candidate-two.md"],
  "decision_authorizations": [],
  "stated_lens_refs": []
}
```

Keep prior records and failed checks. A stacked parent's candidate must match the next baseline; it must be earlier in the same loop, and a stopped or gate-blocked line cannot silently restart. Keep brief, budget, capture conditions/methods and an assumed lens fixed unless the user supplies a correction. Validation cannot establish that two images really were captured identically or that an authority reference is authentic; inspect the artifacts and actual user instructions.
