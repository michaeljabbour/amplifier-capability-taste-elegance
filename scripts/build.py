#!/usr/bin/env python3
"""Build a portable static site and skill bundle using only Python's standard library."""
import argparse
import html
import hashlib
import json
import re
import shutil
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / 'skills/improve-taste-and-elegance'
SKILL_FILES = ('SKILL.md', 'references/calibration.md', 'references/improvement-round.md', 'references/improvement-round.schema.json', 'references/improvement-round.v2.schema.json', 'references/validate_round.py', 'references/delegated-loop.md', 'references/coaching-session.v1.md', 'LICENSE')


def escape(value):
    return html.escape(str(value), quote=True)


def code_cards(versions):
    cards = []
    for item in versions:
        x, y = item['point']
        dots = ''.join(f'<circle cx="{40+(v["point"][0]-1)*50}" cy="{220-(v["point"][1]-1)*50}" r="{7 if v is item else 4}" class="{ "current-dot" if v is item else "other-dot"}"/>' for v in versions)
        plot = f'<svg viewBox="0 0 280 260" role="img" aria-label="Illustrative placement: taste {x}, elegance {y}. Path from original 4,2 to round one 4,3 to round two 4,4. Worse alternative 1,4 is a rejected branch."><path class="mini-grid" d="M40 20V220H240 M40 120H240 M140 20V220"/><path class="mini-route" d="M190 170V70"/>{dots}<text x="140" y="249" text-anchor="middle">Taste →</text><text x="9" y="17">Elegance ↑</text><text x="49" y="64">W</text><text x="203" y="175">0</text><text x="203" y="125">1</text><text x="203" y="75">2</text></svg>'
        cards.append(f'<article class="code-card"><p class="eyebrow">{escape(item["label"])}</p><h3>{escape(item["title"])}</h3><pre tabindex="0" aria-label="{escape(item["label"])} Python code"><code>{escape(item["code"])}</code></pre><figure class="code-placement">{plot}<figcaption><strong>Taste {x} · Elegance {y}</strong><p>{escape(item["why"])}</p><p class="note">Provisional judgment · medium confidence · illustrative, not measured.</p></figcaption></figure><p class="code-gate">{escape(item["gate"])}</p><p><strong>{escape(item["move"])}</strong></p><p class="note">Risk &amp; rollback: {escape(item["risk"])}</p></article>')
    return ''.join(cards)


def evaluation_content(config, skill, calibration):
    relative = config['evaluation']['path']
    folder = ROOT / relative
    data = json.loads((folder / 'results.json').read_text())
    manifests = [json.loads((folder / name).read_text()) for name in ('manifest.json', 'continuations.json', 'stress-manifest.json')]
    runs = {run['run_id']: run for manifest in manifests for run in manifest}
    records = data['results']
    if len(records) != len(runs) or {r['run_id'] for r in records} != set(runs):
        raise ValueError('Evaluation records and task manifest disagree')
    # Headline counts come from case outcomes, not hand-maintained marketing copy.
    skill_runs = [r for r in records if r['run_id'].endswith('-skill')]
    handoffs = [r for r in records if r['run_id'].startswith('H')]
    passed = sum(r['verdict'] == 'pass' for r in skill_runs)
    partial = sum(r['verdict'] == 'mixed' for r in skill_runs)
    critical = sum(r['verdict'] == 'critical_failure' for r in records)
    handoff_pass = sum(r['verdict'] == 'pass' for r in handoffs)
    date = escape(config['evaluation']['date'])
    hashes = json.loads((folder / 'snapshot/hashes.json').read_text())
    matches = all(hashlib.sha256(content.encode('utf-8')).hexdigest() == hashes[name] for name, content in [('SKILL.md', skill), ('references/calibration.md', calibration)])
    status = 'The evaluated skill matches the current download.' if matches else 'The current download has changed since this evaluation. These results apply to the linked snapshot.'
    summary = f'<div class="benefit-summary"><div><p class="eyebrow">What could change in your work?</p><h2 id="evaluation-title">A clearer result.<br>More of your judgment.</h2><p>See how the skill helped an agent preserve a writer’s voice, catch a harmful cleanup, and propose a clearer way into a story.</p><a class="button primary" href="./evidence.html">See the work change</a></div><div class="benefit-preview"><p class="preview-label">An improvement worth noticing</p><blockquote>“The kettle was arguing<br>with the rain.”</blockquote><p>The sentence around it changed.<br>The character stayed.</p><p class="note">From a writing exercise in our evaluation. Reader benefit has not been measured.</p></div></div><details class="home-evidence-note"><summary>What evidence is behind these examples?</summary><p>In our {date} evaluation, {passed} of {len(skill_runs)} skill scenarios fully met the process rubric; {partial} were partial. {handoff_pass} of {len(handoffs)} handoff exercises passed. Across {len(records)} task runs, {critical} critical failures were observed. These are curated exercises reviewed by AI agents and the author. They demonstrate behavior in those exercises; lasting gains in people’s work or capabilities remain unmeasured.</p><p>{status} <a href="./evidence.html#research-record">Read the evaluation record.</a></p></details>'
    labels = {'pass': 'Pass', 'mixed': 'Partial', 'critical_failure': 'Critical failure'}
    rows = []
    for record in sorted(records, key=lambda r: r['run_id']):
        rid = record['run_id']; run = runs[rid]
        kind = 'Control' if rid.endswith('-control') else 'Handoff' if rid.startswith('H') else 'Skill'
        items = ''.join(f'<li><strong>{escape(key)} · {escape(value["rating"])}</strong> — {escape(value["evidence"])}</li>' for key, value in record['checks'].items())
        response = (folder / 'runs' / rid / 'response.md').read_text()
        rows.append(f'<details class="evidence-case"><summary><span>{escape(rid.split("-")[0])} · {escape(run["title"])}</span><span>{kind} · {labels[record["verdict"]]}</span></summary><h3>User request</h3><pre class="evidence-text" tabindex="0">{escape(run["prompt"])}</pre><h3>Adjudicated checks</h3><ul>{items}</ul><details><summary>Read the full response</summary><pre class="evidence-text" tabindex="0">{escape(response)}</pre></details><p><a href="./{relative}/runs/{rid}/execution.md">Execution log (text)</a></p></details>')
    phases = ''.join(f'<tr><th scope="row">{title}</th><td>{data[key]["n"]}</td><td>{data[key]["pass"]}</td><td>{data[key]["mixed"]}</td></tr>' for key, title in [('initial_skill', 'Initial skill cases'), ('initial_controls', 'Initial controls'), ('handoffs', 'Handoff tests'), ('stress_skill', 'Exploratory skill cases'), ('stress_controls', 'Exploratory controls')])
    return {'EVALUATION': summary, 'EVIDENCE_CASES': ''.join(rows), 'EVIDENCE_PHASES': phases, 'EVIDENCE_PATH': escape(relative), 'EVALUATION_DATE': date}


def build(output):
    site = ROOT / 'site'
    config = json.loads((site / 'site.json').read_text(encoding='utf-8'))
    skill = (SKILL_DIR / 'SKILL.md').read_text(encoding='utf-8')
    calibration = (SKILL_DIR / 'references/calibration.md').read_text(encoding='utf-8')
    # The site presents the canonical anchors and questions, not a second rubric.
    taste_block, elegance_block = calibration.split('Taste:\n', 1)[1].split('Elegance:\n', 1)
    taste = re.findall(r'^- [1-5]: (.+)$', taste_block, re.M)
    elegance = re.findall(r'^- [1-5]: (.+)$', elegance_block, re.M)
    questions = re.findall(r'^\d\. (.+)$', calibration, re.M)
    if len(taste) != 5 or len(elegance) != 5 or len(questions) != 8:
        raise ValueError('Expected five canonical anchors per axis and eight questions')
    if not config['examples']:
        raise ValueError('At least one illustrative example is required')
    for example in config['examples']:
        for key in ('before', 'after'):
            if len(example[key]) != 2 or any(type(n) is not int or not 1 <= n <= 5 for n in example[key]):
                raise ValueError('Illustrative coordinates must use two whole anchors from 1 to 5')
        if example['before'] == example['after']:
            raise ValueError('A movement example needs different positions')
    first = config['examples'][0]
    replacements = {
        'CODE_CARDS': code_cards(config['code_walkthrough']),
        'NAME': escape(config['name']),
        'DESCRIPTION': escape(config['description']),
        'DETAIL_URL': escape(config['skill_detail_url']),
        'EXAMPLE_OPTIONS': ''.join(f'<option value="{escape(item["id"])}">{escape(item["label"])}</option>' for item in config['examples']),
        'EXAMPLE_BRIEF': escape(first['brief']),
        'EXAMPLE_DIRECTION': escape(first['direction']),
        'EXAMPLE_TITLE': escape(first['proposal']),
        'EXAMPLE_DETAIL': escape(first['proposal_detail']),
        'ANCHORS': ''.join(f'<li><p><span class="mobile-axis-label">Taste</span>{escape(t)}</p><p><span class="mobile-axis-label">Elegance</span>{escape(e)}</p></li>' for t, e in zip(taste, elegance)),
        'QUESTIONS': ''.join(f'<li>{escape(question)}</li>' for question in questions),
        'SKILL_SOURCE': escape(skill),
    }
    replacements.update(evaluation_content(config, skill, calibration))
    for key in ('bottleneck', 'risk', 'verification', 'growth'):
        replacements['EXAMPLE_' + key.upper()] = escape(first[key])
    page = (site / 'template.html').read_text(encoding='utf-8')
    for key, value in replacements.items():
        page = page.replace('@@' + key + '@@', value)
    if re.search(r'@@[A-Z_]+@@', page):
        raise ValueError('Unresolved template placeholder')
    output.mkdir(parents=True, exist_ok=True)
    assets = output / 'assets'
    assets.mkdir(exist_ok=True)
    (output / 'index.html').write_text(page, encoding='utf-8')
    evidence = (site / 'evidence.html').read_text(encoding='utf-8')
    for key, value in replacements.items():
        evidence = evidence.replace('@@' + key + '@@', value)
    if re.search(r'@@[A-Z_]+@@', evidence):
        raise ValueError('Unresolved evidence page placeholder')
    (output / 'evidence.html').write_text(evidence, encoding='utf-8')
    shutil.copy2(site / 'theme/style.css', assets / 'family.css')
    shutil.copy2(site / 'style.css', assets / 'style.css')
    shutil.copy2(site / 'site.js', assets / 'site.js')
    shutil.copy2(site / 'theme/LICENSE', assets / 'family-LICENSE.txt')
    for asset in sorted((site / 'assets').iterdir()):
        if asset.is_file():
            shutil.copy2(asset, assets / asset.name)
    (assets / 'examples.json').write_text(json.dumps(config['examples'], ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    # Publish the skill at the site root (stable download links) and at its source
    # path (so README links work both on GitHub and on the site).
    for name in SKILL_FILES:
        for target in (output / name, output / SKILL_DIR.relative_to(ROOT) / name):
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(SKILL_DIR / name, target)
    documentation = ['README.md', 'LICENSE', 'site/README.md', 'site/theme/LICENSE']
    documentation.extend(str(path.relative_to(ROOT)) for path in sorted((ROOT / 'docs').glob('*.md')))
    documentation.extend(str(path.relative_to(ROOT)) for path in sorted((ROOT / config['evaluation']['path']).rglob('*')) if path.is_file() and path.suffix in ('.md', '.json', '.txt', '.py'))
    documentation.extend(str(path.relative_to(ROOT)) for path in sorted((ROOT / 'docs/screenshots').glob('*.jpg')))
    for name in documentation:
        target = output / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / name, target)
    (output / '.nojekyll').touch()
    # Fixed archive metadata makes download contents reproducible across builds.
    with ZipFile(output / 'improve-taste-and-elegance.zip', 'w', ZIP_DEFLATED) as bundle:
        for name in SKILL_FILES:
            info = ZipInfo('improve-taste-and-elegance/' + name, (2026, 10, 16, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            bundle.writestr(info, (SKILL_DIR / name).read_bytes())
    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / '_site', help='Static output directory (default: _site)')
    args = parser.parse_args()
    print(f'Built {build(args.output.resolve())}')
