#!/usr/bin/env python3
"""Read-only improvement-record checks. Never executes artifacts or grants authority.

JSON Schema validation uses an already installed `jsonschema` package. Operator
context is supplied independently of the model-produced record; neither this
program nor a matching source reference authenticates that context.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

SCHEMAS = {
    'improvement-round/v1': 'improvement-round.schema.json',
    'improvement-round/v2': 'improvement-round.v2.schema.json',
}
MAX_BYTES = 1024 * 1024


class RoundValidationError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise RoundValidationError(message)


def read_json(path):
    selected = Path(path)
    require(selected.stat().st_size <= MAX_BYTES, 'Selected JSON file exceeds 1 MiB')
    data = selected.read_bytes()
    require(len(data) <= MAX_BYTES, 'Selected JSON file exceeds 1 MiB')

    def unique(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, 'Duplicate JSON key: ' + key)
            result[key] = value
        return result

    return json.loads(data.decode('utf-8'), object_pairs_hook=unique)


def structural(record):
    require(isinstance(record, dict), 'Record must be an object')
    version = record.get('schema_version')
    require(isinstance(version, str) and version in SCHEMAS, 'Unsupported schema_version')
    try:
        from jsonschema import Draft202012Validator
    except ImportError as error:
        raise RoundValidationError('JSON Schema engine unavailable: use an existing environment with jsonschema; nothing was installed') from error
    # Only package-owned schemas are loaded. No record-supplied schema or remote
    # reference is resolved; the canonical schemas have no external references.
    schema = json.loads((Path(__file__).parent / SCHEMAS[version]).read_text())
    Draft202012Validator.check_schema(schema)
    errors = sorted(Draft202012Validator(schema).iter_errors(record), key=lambda e: str(list(e.path)))
    require(not errors, '; '.join('/'.join(map(str, e.path)) + ': ' + e.message for e in errors))


def context_values(context):
    require(isinstance(context, dict), 'Independent operator context is required')
    require(set(context) <= {'max_rounds', 'artifact_refs', 'decision_authorizations', 'stated_lens_refs'}, 'Unknown operator-context property')
    limit = context.get('max_rounds', 2)
    require(type(limit) is int and limit >= 1, 'Operator max_rounds must be a positive integer')
    artifacts = context.get('artifact_refs')
    require(isinstance(artifacts, list) and artifacts and all(isinstance(x, str) and x for x in artifacts), 'Operator artifact_refs must explicitly list the permitted artifact/rollback references')
    authorizations = context.get('decision_authorizations', [])
    require(isinstance(authorizations, list), 'Operator decision_authorizations must be a list')
    for item in authorizations:
        require(isinstance(item, dict) and set(item) == {'action', 'authority', 'source_ref'}, 'Decision authorization needs exactly action, authority and source_ref')
        require(item['action'] in {'keep', 'undo'} and item['authority'] in {'human', 'delegated'} and isinstance(item['source_ref'], str) and item['source_ref'], 'Invalid decision authorization metadata')
    lens_refs = context.get('stated_lens_refs', [])
    require(isinstance(lens_refs, list) and all(isinstance(x, str) and x for x in lens_refs), 'Operator stated_lens_refs must be a list of references')
    return limit, set(artifacts), authorizations, set(lens_refs)


def capture_conditions(record):
    return {(x['condition'], x['method']) for x in record['comparison'].get('captures', [])}


def validate_record(record, context, previous=()):
    structural(record)
    limit, permitted, authorizations, stated_lenses = context_values(context)
    require(record['comparison']['brief_ref'] == record['brief']['source_ref'], 'Comparison must use the same brief source reference')
    gate_ids = [x['id'] for x in record['gates']]
    require(len(gate_ids) == len(set(gate_ids)), 'Gate IDs must be unique')
    budget = record['budget']
    require(budget['rounds_limit'] <= limit, 'Record exceeds the independently supplied round budget (default two)')
    require(budget['rounds_used'] <= budget['rounds_limit'], 'rounds_used exceeds rounds_limit')
    require(budget['rounds_used'] < budget['rounds_limit'] or budget['stop_reason'] != 'continue', 'Exhausted budget cannot continue')
    refs = {record['baseline']['artifact_ref'], record['candidate']['artifact_ref'], record['decision']['rollback_ref']}
    captures = record['comparison'].get('captures', [])
    for capture in captures:
        refs.update((capture['baseline_ref'], capture['candidate_ref']))
    require(refs <= permitted, 'Artifact or rollback reference is outside independently supplied scope')
    conditions = [x['condition'] for x in captures]
    require(len(conditions) == len(set(conditions)), 'Capture conditions must be unique')
    decision = record['decision']
    if decision['action'] in {'keep', 'undo'}:
        needed = {k: decision[k] for k in ('action', 'authority', 'source_ref')}
        require(needed in authorizations, 'Keep/undo lacks matching independently supplied decision authorization metadata')
    if record['schema_version'] == 'improvement-round/v2' and decision['action'] in {'proposed', 'defer'}:
        require(decision['authority'] == 'none', 'Proposed/deferred records use no authority')

    history = list(previous)
    for old in history:
        structural(old)
        if old['round_id'] == record['round_id']:
            require(old['baseline'] == record['baseline'], 'Baseline changed within a round ID')
    loop = record.get('loop')
    if loop:
        same = [x for x in history if x.get('loop', {}).get('id') == loop['id']]
        unique_rounds = {x['round_id'] for x in same} | {record['round_id']}
        require(budget['rounds_used'] == len(unique_rounds), 'Loop budget must count every unique round, including proposals')
        for old in same:
            require(old['brief']['source_ref'] == record['brief']['source_ref'], 'Loop brief changed')
            require(old['budget']['rounds_limit'] == budget['rounds_limit'], 'Loop round budget changed')
            require(capture_conditions(old) == capture_conditions(record), 'Loop capture conditions or methods changed')
            if old['brief']['lens_status'] == 'assumed' and record['brief']['lens_status'] != 'assumed':
                require(record['brief'].get('lens_ref') in stated_lenses, 'Assumed lens cannot become stated without operator-supplied correction provenance')
        parent_id = loop.get('parent_round_id')
        if parent_id:
            parents = [x for x in same if x['round_id'] == parent_id]
            require(len(parents) == 1, 'Stacked parent must identify one earlier round in this loop')
            parent = parents[0]
            require(parent['budget']['rounds_used'] < budget['rounds_used'], 'Parent must precede the child round')
            require(parent['candidate'] == record['baseline'], 'Stacked parent candidate does not match child baseline')
            require(parent['budget']['stop_reason'] == 'continue', 'A stopped line of rounds cannot silently continue')
            require(not any(g['critical'] and g['status'] in {'fail', 'unknown'} for g in parent['gates']), 'Critical failed/unknown parent gate stops this line')
    return {'status': 'pass', 'schema_version': record['schema_version'], 'scope': 'record-conformance-and-metadata-consistency-only', 'runtime_authorization': False}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('record', type=Path)
    parser.add_argument('--context', type=Path, required=True, help='Separately supplied operator metadata; never derive it from the record')
    parser.add_argument('--previous', type=Path, action='append', default=[])
    args = parser.parse_args(argv)
    try:
        result = validate_record(read_json(args.record), read_json(args.context), [read_json(p) for p in args.previous])
        print(json.dumps(result, sort_keys=True))
        return 0
    except (RoundValidationError, ValueError, OSError, UnicodeError, TypeError, KeyError) as error:
        print(json.dumps({'status': 'fail', 'error': str(error), 'runtime_authorization': False}, sort_keys=True), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
