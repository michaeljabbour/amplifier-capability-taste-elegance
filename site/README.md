# Website

This page follows the reference project's static Python build, Amplifier family
visual language, two-column hero, local assets, fine rules, and restrained navigation.
The generated `_site/` directory is compatible with static hosting, including a
repository subpath on GitHub Pages. All product links are relative or page anchors.
The public repository uses `.github/workflows/pages.yml` to build, check, and
publish `_site/` from `main` with GitHub Pages. The repository About website and
the first README link point to the site.

## Build and preview

From the repository root with Python 3.11 or later:

```sh
python3 scripts/build.py
python3 scripts/check.py
python3 -m http.server 8000 --bind 127.0.0.1 --directory _site
```

Open `http://127.0.0.1:8000`. The build uses only Python's standard library.
The example selector fetches a local JSON asset, so preview over HTTP rather than
opening the HTML with `file://`.

## Edit

- `site.json`: metadata and explicitly fictional examples.
- `template.html`: semantic page content and layout.
- `evidence.html`: visual work examples and the judgments they help people practice,
  with benchmark methods and case records in an optional disclosure.
- `../docs/evaluations/benchmark-2026-10-17/`: frozen results and source evidence.
  The build derives headline counts from `results.json`, includes the benchmark
  archive, and marks whether the evaluated snapshot matches the current download.
- `style.css`: product styles and responsive behavior.
- `site.js`: native example selection, baseline/proposed views, copy feedback.
- `assets/`: original SVG favicon and share illustration. Some social platforms
  require raster share images; no claim of platform support is made for the SVG.
- `../skills/improve-taste-and-elegance/SKILL.md` and its `references/calibration.md`: source for the download, bundle,
  embedded source, optional qualitative anchors, and eight invitations. Do not fork the rubric
  into another content file.

## Theme provenance

`theme/style.css` is an unmodified snapshot of Amplifier Smart Tools family theme
v0.1.0, copied from the local Decisioncraft reference project. `theme/LICENSE`
retains its original MIT notice. The product-specific template, graph, SVG assets,
and styles are new. We did not copy Decisioncraft's content, videos, credentials,
repository metadata, or institutional attribution.

## Design notes

- Paper `#f6f4ee`, ink `#252823`, muted `#64685e`, rules `#d8d8cc`,
  gold `#80642f`, sage accent `#486b61`; these preserve the reference palette.
- Georgia headings and Arial body, system fallbacks, no font requests.
- The map is the one expressive element. The rest supports reading and using the skill.
- Desktop pairs the map with a short example panel; phones stack both in reading order.
- The map is a conversation aid. Its form example illustrates gentle refinement;
  its workflow example illustrates a conceptual jump. Neither path is measured.
  Provisional judgments require the user's experience and reasoning, a shared brief,
  gate status, evidence, confidence, and missing evidence. The user retains agency.
- No automatic movement. State changes follow explicit native controls. Reduced
  motion disables smooth scrolling. A text example remains without JavaScript.

## Deployment

The Pages source is GitHub Actions. The workflow separates build and deployment
jobs, checks the output before upload, and uploads only `_site/`. Deployment gets
`pages: write` and `id-token: write`; the build has read access only. No project
secrets or backend services are needed. Official GitHub action revisions are
pinned to fixed commits. Future pushes to `main` rebuild and redeploy the site;
manual runs are also available from Actions.

The live URL is <https://michaeljabbour.github.io/amplifier-capability-taste-elegance/>. Keep
asset, navigation, and download paths relative so repository-subpath hosting works.
