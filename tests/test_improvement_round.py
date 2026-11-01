"""Deterministic record/compatibility tests; no provider or human-effect claims."""
from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
REFS = ROOT / 'skills/improve-taste-and-elegance/references'
SPEC = importlib.util.spec_from_file_location('validate_round', REFS / 'validate_round.py')
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


def record(version='v2'):
    data = {
        'schema_version': 'improvement-round/' + version,
        'round_id': 'round-one',
        'brief': {'intent': 'Clarify a fictional outage notice without losing warmth', 'audience': 'Library visitors', 'source_ref': 'brief.md', 'lens_status': 'assumed', 'must_preserve': ['Keep the acknowledgement']},
        'baseline': {'artifact_ref': 'baseline.md', 'sha256': 'a' * 64},
        'candidate': {'artifact_ref': 'candidate-one.md', 'sha256': 'b' * 64},
        'change': {'mode': 'hillclimb', 'hypothesis': 'Move the next action first', 'predicted_benefit': 'The action may be easier to find', 'regression_risk': 'The notice may lose warmth'},
        'gates': [{'id': 'correctness', 'critical': True, 'status': 'pass', 'evidence_ref': 'checks.txt', 'reason': 'Exact required facts retained'}],
        'comparison': {'brief_ref': 'brief.md', 'observations': ['No reader study ran'], 'taste': {'status': 'hypothesis', 'reason': 'The acknowledgement remains'}, 'elegance': {'status': 'unknown', 'reason': 'Reader effort is not measured'}},
        'decision': {'action': 'proposed', 'authority': 'none', 'source_ref': 'brief.md', 'reason': 'Review together', 'rollback_ref': 'baseline.md'},
        'budget': {'rounds_limit': 2, 'rounds_used': 1, 'stop_reason': 'continue'},
    }
    if version == 'v2':
        data['loop'] = {'id': 'fictional-loop'}
        data['brief']['lens_ref'] = 'brief.md#assumptions'
        data['comparison']['captures'] = [{'condition': 'same excerpt', 'method': 'plain text comparison', 'baseline_ref': 'baseline.md', 'candidate_ref': 'candidate-one.md'}]
    return data


def context():
    return {'artifact_refs': ['baseline.md', 'candidate-one.md', 'candidate-two.md'], 'decision_authorizations': []}


def second(first):
    result = deepcopy(first)
    result['round_id'] = 'round-two'
    result['loop']['parent_round_id'] = first['round_id']
    result['baseline'] = deepcopy(first['candidate'])
    result['candidate'] = {'artifact_ref': 'candidate-two.md', 'sha256': 'c' * 64}
    result['comparison']['captures'][0].update(baseline_ref='candidate-one.md', candidate_ref='candidate-two.md')
    result['budget'].update(rounds_used=2, stop_reason='budget-exhausted')
    return result


class ContractTests(unittest.TestCase):
    def assertRejected(self, data, operator=None, previous=()):
        with self.assertRaises(module.RoundValidationError):
            module.validate_record(data, context() if operator is None else operator, previous)

    def test_v1_is_byte_identical_to_published_contract(self):
        # Pin captured from public main712d9c6; a closed version never grows in place.
        self.assertEqual('0ba57926a11b35029572208330cea8c15564559aaf47e1f99a3224f2c2674be0', hashlib.sha256((REFS / 'improvement-round.schema.json').read_bytes()).hexdigest())
        schema = json.loads((REFS / 'improvement-round.schema.json').read_text())
        self.assertEqual('urn:amplifier:improvement-round:v1', schema['$id'])
        self.assertNotIn('loop', schema['properties'])

    def test_existing_v1_record_still_valid(self):
        self.assertEqual('pass', module.validate_record(record('v1'), context())['status'])

    def test_versions_and_pointers_are_explicit(self):
        for v in ['v1', 'v2']:
            pointer = json.loads((ROOT / f'contracts/improvement-round.{v}.json').read_text())
            schema = json.loads((ROOT / 'contracts' / pointer['$ref']).read_text())
            self.assertEqual('urn:amplifier:improvement-round:' + v, schema['$id'])
            self.assertEqual('improvement-round/' + v, schema['properties']['schema_version']['const'])

    def test_v1_rejects_delegated_extension_even_when_fields_optional_in_v2(self):
        data = record(); data['schema_version'] = 'improvement-round/v1'
        self.assertRejected(data)

    def test_v2_default_is_explicit_proposal_without_runtime_authority(self):
        data = record(); before = deepcopy(data)
        result = module.validate_record(data, context())
        self.assertFalse(result['runtime_authorization'])
        self.assertEqual('proposed', data['decision']['action'])
        self.assertEqual('none', data['decision']['authority'])
        self.assertEqual(before, data)

    def test_defaults_never_fill_missing_required_decision(self):
        data = record(); del data['decision']['action']
        self.assertRejected(data)

    def test_unknown_fields_rejected_at_each_added_boundary(self):
        for where in ['root', 'loop', 'brief', 'comparison', 'capture']:
            with self.subTest(where=where):
                data = record()
                target = {'root': data, 'loop': data['loop'], 'brief': data['brief'], 'comparison': data['comparison'], 'capture': data['comparison']['captures'][0]}[where]
                target['unexpected'] = True
                self.assertRejected(data)

    def test_capture_needs_named_method(self):
        data = record(); del data['comparison']['captures'][0]['method']
        self.assertRejected(data)

    def test_keep_or_undo_cannot_self_authorize(self):
        for action in ['keep', 'undo']:
            with self.subTest(action=action):
                data = record(); data['decision'].update(action=action, authority='delegated', source_ref='brief.md#permission')
                self.assertRejected(data)
                operator = context(); operator['decision_authorizations'] = [{'action': action, 'authority': 'delegated', 'source_ref': 'different.md'}]
                self.assertRejected(data, operator)

    def test_independent_authorization_metadata_does_not_grant_runtime_permission(self):
        data = record(); data['decision'].update(action='keep', authority='delegated', source_ref='brief.md#permission')
        operator = context(); operator['decision_authorizations'] = [{'action': 'keep', 'authority': 'delegated', 'source_ref': 'brief.md#permission'}]
        self.assertFalse(module.validate_record(data, operator)['runtime_authorization'])

    def test_critical_fail_and_unknown_block_keep_and_continuation(self):
        for status in ['fail', 'unknown']:
            with self.subTest(status=status):
                data = record(); data['gates'][0]['status'] = status
                self.assertRejected(data)  # Proposed rounds still cannot continue the line.
                data['budget']['stop_reason'] = 'gate-blocked'
                self.assertEqual('pass', module.validate_record(data, context())['status'])
                data['decision'].update(action='keep', authority='human')
                operator = context(); operator['decision_authorizations'] = [{'action': 'keep', 'authority': 'human', 'source_ref': 'brief.md'}]
                self.assertRejected(data, operator)

    def test_duplicate_gate_and_changed_brief_rejected(self):
        data = record(); data['gates'].append(deepcopy(data['gates'][0])); self.assertRejected(data)
        data = record(); data['comparison']['brief_ref'] = 'other.md'; self.assertRejected(data)

    def test_default_two_round_budget_not_replaced_by_record(self):
        data = record(); data['budget']['rounds_limit'] = 3
        self.assertRejected(data)
        operator = context(); operator['max_rounds'] = 3
        self.assertEqual('pass', module.validate_record(data, operator)['status'])

    def test_used_exceeds_limit_and_exhausted_continue_rejected(self):
        data = record(); data['budget']['rounds_used'] = 3; self.assertRejected(data)
        data = record(); data['budget']['rounds_used'] = 2; self.assertRejected(data)
        data = record(); data['budget']['rounds_limit'] = True; self.assertRejected(data)

    def test_scope_checked_independently_for_artifacts_rollback_and_captures(self):
        for field in ['candidate', 'rollback', 'capture']:
            with self.subTest(field=field):
                data = record()
                if field == 'candidate': data['candidate']['artifact_ref'] = '../outside.md'
                elif field == 'rollback': data['decision']['rollback_ref'] = '../outside.md'
                else: data['comparison']['captures'][0]['candidate_ref'] = '../outside.md'
                self.assertRejected(data)
        self.assertRejected(record(), {})

    def test_same_round_baseline_cannot_change(self):
        old = record(); data = deepcopy(old); data['baseline']['sha256'] = 'd' * 64
        self.assertRejected(data, previous=[old])

    def test_stacked_second_round_preserves_two_round_stop(self):
        first = record(); result = second(first)
        self.assertEqual('pass', module.validate_record(result, context(), [first])['status'])

    def test_proposals_count_and_parent_must_precede_and_match(self):
        first = record(); result = second(first); result['budget']['rounds_used'] = 1
        self.assertRejected(result, previous=[first])
        result = second(first); result['baseline']['sha256'] = 'd' * 64
        self.assertRejected(result, previous=[first])
        result = second(first); result['loop']['parent_round_id'] = 'future'
        self.assertRejected(result, previous=[first])

    def test_fixed_conditions_methods_and_brief_stay_fixed(self):
        first = record()
        for field in ['condition', 'method', 'brief', 'budget']:
            with self.subTest(field=field):
                result = second(first)
                if field in ['condition', 'method']: result['comparison']['captures'][0][field] = 'changed'
                elif field == 'brief': result['brief']['source_ref'] = result['comparison']['brief_ref'] = 'changed.md'
                else: result['budget']['rounds_limit'] = 3
                operator = context(); operator['max_rounds'] = 3
                self.assertRejected(result, operator, [first])

    def test_stopped_or_critical_parent_cannot_stack(self):
        first = record(); first['budget']['stop_reason'] = 'no-meaningful-gain'
        self.assertRejected(second(first), previous=[first])
        first = record(); first['gates'][0]['status'] = 'unknown'
        self.assertRejected(second(first), previous=[first])

    def test_assumed_lens_needs_independent_correction_reference(self):
        first = record(); result = second(first); result['brief'].update(lens_status='stated', lens_ref='user-correction.md')
        self.assertRejected(result, previous=[first])
        operator = context(); operator['stated_lens_refs'] = ['user-correction.md']
        self.assertEqual('pass', module.validate_record(result, operator, [first])['status'])

    def test_cli_reads_selected_records_without_modifying_them(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp); selected = base / 'round.json'; operator = base / 'operator.json'
            selected.write_text(json.dumps(record())); operator.write_text(json.dumps(context()))
            before = selected.read_bytes(), operator.read_bytes()
            result = subprocess.run([sys.executable, str(REFS / 'validate_round.py'), str(selected), '--context', str(operator)], capture_output=True, text=True, timeout=15)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertFalse(json.loads(result.stdout)['runtime_authorization'])
            self.assertEqual(before, (selected.read_bytes(), operator.read_bytes()))

    def test_cli_scope_violation_is_failure_not_an_executable_decision(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp); selected = base / 'round.json'; operator = base / 'operator.json'
            data = record(); data['candidate']['artifact_ref'] = '../outside.md'
            selected.write_text(json.dumps(data)); operator.write_text(json.dumps(context()))
            result = subprocess.run([sys.executable, str(REFS / 'validate_round.py'), str(selected), '--context', str(operator)], capture_output=True, text=True, timeout=15)
            self.assertEqual(2, result.returncode)
            self.assertFalse(json.loads(result.stderr)['runtime_authorization'])
            self.assertFalse((base.parent / 'outside.md').exists())

    def test_duplicate_json_keys_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'duplicate.json'; path.write_text('{"authority":"none","authority":"human"}')
            with self.assertRaises(module.RoundValidationError): module.read_json(path)


if __name__ == '__main__':
    unittest.main()
