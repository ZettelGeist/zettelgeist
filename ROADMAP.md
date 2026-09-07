# ZettelGeist Roadmap

**Status:** Phase 0 shipped as 1.1.6 on 2 September 2026. Phase 1 landed on
6 September 2026. Phases 2–5 are open.

This document is the plan for bringing ZettelGeist up to date: what is wrong with
the codebase today, the order in which to fix it, and the reasoning behind that
order. It is deliberately opinionated and deliberately evidence-bearing — every
finding below was checked against the working tree rather than inferred, and the
evidence is kept in place so that a decision can be re-argued instead of
re-discovered.

Its readership is small: the maintainers, the contributors named in it, and the
coding agents working in this repository. Agents should read
[AGENTS.md](AGENTS.md) first for how to work here, and this file for what to work
on.

The five phases that follow the completed Phase 0 are ordered so that nothing
risky ships before the release path can catch it. Each is independently
mergeable and ends at a taggable state. This is a point of departure, not a
terminus — the campaign after this one gets appended here rather than starting a
new document.

---

## What the code says

Assessed against `dev` @ `7e1ab64` on 1 September 2026, on Python 3.12.3 with
PyYAML 6.0.2 and Tatsu 5.13.1. At the time of assessment: version 1.1.5, 1,509
LOC in the package, 9 open issues, 4 commits unmerged on `dev`, a test suite that
could not execute, no CI test job, and one stale pull request.

### Issue 38 — the ZQL grammar throws away every word but the last

The `literal` rule in `zdb.py:211` uses a capturing group: `/"(\s+|\w+)*"/`.
Modern Tatsu returns group 1 rather than the whole match, so a quoted phrase
collapses to its final repetition. This is the entire mystery of issue 38 — the
reported counts of 29 and 9 reproduce exactly against the baseball zettels in
`deprecated/docs/example/mlb`.

```
# zquery.compile() today
tags:"AL Central"  =>  MATCH 'tags:Central'                 → 9 hits

# after changing the group to non-capturing: (?:\s+|\w+)*
tags:"AL Central"  =>  MATCH 'tags:AL NEAR/1 tags:Central'  → 5 hits ✓
```

The fix was verified in a scratch process; it is a two-character edit. The
remaining half of issue 38 is structural and belongs in Phase 3.

### Index — list fields are flattened, so phrases match across tag boundaries

`zdb.py` stores tags as one comma-joined string (`MLB,National League,NL
Central`) in an fts4 table. The tokenizer sees no boundary at the comma, so the
last word of one tag sits adjacent to the first word of the next and satisfies a
phrase or `NEAR` query. Fixing the grammar narrows the false positives but cannot
remove them; fts5 with a real column filter can.

```
fts4:  tags:"AL Central"    → 0 hits (column prefix is literal)
fts5:  {tags}:"AL Central"  → exact phrase, correct hits
```

### Release — the only workflow builds and can publish, but never tests

`.github/workflows/release.yml` triggers on every `push`, pins Python 3.10.4, and
uploads to PyPI on any tag. There is no `pytest` step anywhere in the repo, and
the suite could not pass if there were one: `tests/test_zettelgeist.py` calls
`yaml.load(doc)` with a single argument, which PyYAML 6 removed. The README still
says CI is "coming soon."

### Packaging — `setup.py`-only, and PyYAML is an undeclared dependency

Every module imports `yaml`, but `install_requires` lists only
`python-frontmatter` and `tatsu`. It works solely because `frontmatter` pulls
PyYAML in transitively — the version that just broke the tests is therefore
unpinned and unowned. `setup.cfg` is empty, `scripts/deploy.sh` still calls the
deprecated `setup.py sdist bdist_wheel`, and `bin/` holds four shims that
duplicate the declared `console_scripts`.

### Runtime — small latent breakages

`zutils.md5_for_file()` calls `hashlib.md5()` but `hashlib` is never imported —
the function raises `NameError` the first time anyone uses it. `zdb.GRAMMAR` is a
plain string containing `\s`, which already emits a `SyntaxWarning` on Python
3.12 and becomes an error later. `zquery.py` uses `tempfile.mktemp()`, deprecated
since 2.3. Both `zettel.py` and `zquery.py` import `readline` unconditionally,
which does not exist on Windows.

### Style — the code predates most of the Python it now runs on

Zero f-strings and 69 `%`-format sites; zero type annotations; 8 bare `except:`
clauses that swallow everything including `KeyboardInterrupt`; `from .zutils
import *` in `zfind.py`; and `zettel.py`'s `main()` runs 240 lines of the file's
761. Diagnostics go to `print()` in 45 places, which is why issue 41 exists —
there is no verbosity level to turn down.

### Repo — roughly half the tracked tree is dead

92 tracked files, of which `project/*.sbt` is a Scala build, `deprecated/` is a
retired Jekyll site plus an old module, `sphinx-docs/` duplicates content now
living in the wiki, and `src/` holds a single stray `ps.text` — a name that will
collide the day the package moves to a src layout. `BETA.md` instructs the reader
to source a `setpath.sh` that no longer exists.

---

## The phases

### Phase 0 — Land the work that is already done ✅

**Merged and tagged 2 September 2026 as 1.1.6**
([#44](https://github.com/ZettelGeist/zettelgeist/pull/44)). *Not yet published:*
the release workflow failed at the PyPI upload with a 403 — the account behind
the stored API token has no verified primary email — and the GitHub release step
was skipped in consequence. PyPI still serves 1.1.5. See Phase 2 for the fix.

Four commits had sat on `dev` since August 2024, unmerged and unreleased: Unicode
in `yaml.dump`, YAML for `.counter.dat`, `--counter` inheriting `--id`, and the
`zimport` summary line. They were merged to `master`, `zversion.py` was bumped,
and 1.1.6 was tagged following `docs/RELEASING.md`.

*Closed: 37, 39, 42. Issue 41 left open — the summary line is the smaller half of
it.*

### Phase 1 — Prune the tree ✅

**Landed 6 September 2026.** 92 tracked files became 57. The package, the
tests, `docs/` and `.github/` are all that remain, plus `bin/` and `scripts/`,
which Phase 2 takes. No behavior change: import, query, `--get-all-tags` and
`zettel` output over the mlb corpus are byte-identical across the whole phase,
including the 9 hits for `tags:"AL Central"` and the 29 for
`tags:"National League"` recorded above.

Three latent crashes turned up while checking the README's examples against a
real checkout. None was previously recorded, none is fixed here, and all three
are Phase 5 work: `zettel --file` on a note with an unknown field prints the
right diagnostic and then dies with an `UnboundLocalError`; `zfind --publish`
raises `TypeError` on any matched note carrying a `cite` field unless
`--publish-conf` is given, because `reformat_cite()` builds its template from
`cite_format.get('before')`, which is `None` with no configuration loaded; and
`zimport --validate` creates the database file despite indexing nothing.

Two departures from the plan as written, both in the direction of not landing a
broken gate:

- **PR #43's community files could not be harvested, only its idea.**
  `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `SUPPORT.md` and
  `GOVERNANCE.md` are zero-byte files in that branch; `CITATION.cff` is one
  comment; `CODEOWNERS` and `FUNDING.yml` are GitHub's own documentation
  examples, `@octocat` included. Those six were written from scratch against
  this project instead; `CODEOWNERS` and `FUNDING.yml` were not taken at all.
  `GOVERNANCE.md` describes current practice and wants the maintainer's
  confirmation.
- **Three of PR #43's pre-commit hooks were left out**, with the reasoning
  recorded at the top of `.pre-commit-config.yaml`. flake8 and bandit report
  ~120 and 23 findings against the package as it stands — almost entirely the
  legacy style Phase 5 modernizes, or bandit reading the ZQL-built SQL as
  injection and `md5_for_file()`'s checksum as a security hash. mdformat
  rewrites this file's `---` rules into 70-character underscores and renumbers
  its ordered lists. Deciding the linter question is already Phase 2's job; it
  now also owns adding a linter hook that passes.

*Risk: none — no behavior change. Value: every later phase greps, reviews and
builds a smaller tree.*

Delete `project/` (Scala), `deprecated/`, `sphinx-docs/`, `jupyter/`, `adhoc/`,
`zdb_funcs.sh`, `BETA.md`, and the stray `src/ps.text`. Apply the formatting pass
across the package. Add the community files. All three pieces are harvested from
PR #43 rather than redone — see [Pull request #43](#pull-request-43) below.

Before `deprecated/` can go, **move the 29 baseball zettels in
`deprecated/docs/example/mlb` to `tests/fixtures/mlb/`**, where Phase 3 promotes
them to a real fixture. PR #43 deletes them along with everything else; that
deletion must not be taken.

Two other paths PR #43 removes and this phase must keep: `docs/index.html` and
`docs/.nojekyll`, which together are the live GitHub Pages redirect to the wiki,
and `docs/RELEASING.md`, which is still the release procedure.

Rewrite the README against what the tool does today.

**Why this moved ahead of the build work.** It was Phase 4 in the original plan,
on the reasoning that source changes want a test net under them. That reasoning
applies to the *source modernization* half of the old Phase 4, not to deletions
and a mechanical reformat, which the package either survives or does not. Two
arguments moved it here:

1. A repo-wide reformat conflicts with every branch in flight. Nothing is in
   flight right now. Doing it after Phases 2–4 means rebasing that formatting
   across three phases of real work.
2. PR #43's author is available now. Harvesting his contribution while he is
   around to review the split is worth more than harvesting it in a year.

*Closed: no issues. Superseded PR #43, which can now be closed with a link to
[Pull request #43](#pull-request-43).*

### Phase 2 — Make the build tell the truth

*Unblocks: every phase below. Nothing after this is safe to attempt while a tag
can publish untested code and the test suite cannot execute.*

- Replace `setup.py` with `pyproject.toml`, moving metadata into a PEP 621
  `[project]` table on a standard build backend (setuptools or hatchling).
  Declare `PyYAML>=6` explicitly and put a floor under `tatsu` — the current
  breakage is a Tatsu upgrade nobody pinned. Replace the deprecated license
  classifier with an SPDX `license` field, and set
  `long_description_content_type`, which `twine check` already warns about.
- **Adopt `uv` as the workflow tool** — environments, dependency resolution, the
  `uv.lock` used by CI, the 3.10–3.13 test matrix via `uv python install`, and
  optionally `uv publish`. The argument is specific to this project rather than
  general enthusiasm: the breakage that started this whole effort was an unpinned
  Tatsu upgrade nobody noticed, and a lockfile in CI is what turns that from
  silent rot into a red build.

  Two boundaries on it, which are easy to lose by treating uv as one decision
  instead of two:

  - **uv drives the workflow; it is not the build backend.** Keep a standard
    PEP 621 declaration on setuptools or hatchling so `pip install -e .` and
    `pip install zettelgeist` keep working untouched, contributors are not
    required to have uv, and leaving uv later costs a deleted lockfile rather
    than redone packaging. `uv_build` is the newer and less exercised piece of
    that toolchain, and it buys a library of this size very little.
  - **The lockfile governs CI and development, not installs.** Users get
    whatever `[project.dependencies]` says, so the version floors above still
    have to be right. uv makes drift visible; it does not pin anything for
    consumers.

  Choosing uv also settles PR #43's packaging question in the negative for good:
  its `poetry.lock` is not among the things harvested.
- Repair the tests: `yaml.safe_load` in place of the one-argument `yaml.load`,
  and delete the vestigial `test_mytest`, which asserts that `SystemExit` raises
  `SystemExit`.
- Split CI in two: `ci.yml` runs pytest and the linter on push and pull request
  across 3.10–3.13; `release.yml` triggers only on `v*` tags and moves to PyPI
  trusted publishing instead of a stored token. Refresh `actions/checkout@v2` and
  `actions/setup-python@v2` while there — both target the deprecated Node 20 and
  are being forced onto Node 24.

  Trusted publishing is the higher-value half of that bullet, and it is
  independent of uv. The 1.1.6 tag failed to publish with a 403 because the
  PyPI account behind `secrets.PYPI_API_TOKEN` has no verified primary email; the
  same run also reported that the token disabled Trusted Publishing and with it
  the attestations the action would otherwise have produced. Moving to trusted
  publishing retires the token that failed.
- Settle the formatter and linter question. Phase 1 landed PR #43's
  Black/isort result and a `.pre-commit-config.yaml` carrying isort and Black
  only — no linter, because neither flake8 nor bandit passes on this tree
  today. Decide here whether `ruff format` replaces Black or the two coexist,
  pick the linter, configure it so that it is green on the code as it stands
  (deferring the rest to Phase 5 rather than suppressing it), and make the
  pre-commit config and CI agree. `pyroma` is worth adding once there is a
  `pyproject.toml` for it to check.
- Delete `bin/` and `scripts/deploy.sh`; the entry points and the workflow
  already cover both.
- Turn the README build-status placeholder into a real badge.

### Phase 3 — Fix search

*Closes: 38. This is the only open bug that makes the tool return wrong answers
quietly. Ship the one-line half immediately; take the structural half
deliberately.*

- Make the literal group non-capturing and the grammar a raw string. Land this
  alone, with regression tests asserting the compiled SQL for a set of
  representative queries — the bug was invisible because nothing ever inspected
  that string.
- Migrate `zdb.py` from fts4 to fts5, and emit true phrase queries —
  `{tags}:"AL Central"` — instead of rewriting phrases into `NEAR/1` proximity,
  which is a different question than the user asked. This also retires
  `offsets()`, which fts5 does not have, in favor of its `snippet()` and
  `highlight()`.
- Stop list fields from bleeding into each other across the comma join, so a
  phrase can no longer span two adjacent tags.
- Promote the baseball zettels moved in Phase 1 to a test fixture and assert
  exact result counts per query. They are at `tests/fixtures/mlb/`, and
  `tests/fixtures/README.md` records their provenance and the defect in the
  data. Read [Before Phase 3](#before-phase-3-check-the-fixture-corpus) before
  writing those assertions.

*Note: fts5 forces a reindex, which `zdb.py` already documents as expected — the
index is declared ephemeral.*

### Phase 4 — Give the tools a workspace

*Closes: 31, 33, 34, 35, 41. Five of the nine open issues are one wish stated
five ways: the commands demand too much typing and keep their state in the wrong
place. Issue 33 is the keystone — do it first and the rest get smaller.*

- **Issue 33** — a `.zettelgeist/` directory with a config file, created by a new
  `zettelgeist init`, holding the defaults each command currently demands on
  every invocation. `.counter.dat` and the database move inside it. Now that the
  counter file is YAML (Phase 0), config and counter can share a loader.
- **Issue 31** — short flags `-d` and `-q`. Trivial once argparse setup is
  centralized rather than assembled per module.
- **Issue 34** — replace the fifteen generated `--show-FIELD` flags with
  `--show FIELD...`, bare `--show` meaning all. Keep the old flags as hidden
  aliases for one release.
- **Issue 35** — generate a UUID into each new zettel's metadata, plus a backfill
  mode for existing notes. Index it so `zfind` can address a single document by
  identity rather than by filename.
- **Issue 41** — replace `print()` with the `logging` module: milestone progress
  above a file-count threshold, errors to a log, `-v` to restore per-file output.
- Retire `zcreate`, which already prints its own deprecation notice on every run.

*Note: the only phase with user-visible CLI changes; worth a minor version.*

### Phase 5 — Modernize the source

*Closes: no issues. No behavior change. Best done incrementally, one module per
pull request, now that the tests from Phases 2 and 3 exist to catch mistakes.*

- Fix the latent breakages: `import hashlib`, replace `tempfile.mktemp()` with
  `NamedTemporaryFile`, guard the `readline` imports, and replace the 8 bare
  `except:` clauses with the exceptions actually being caught.
- Move to a `src/zettelgeist/` layout — the old `src/` is already gone in
  Phase 1, so the name is free.
- `%`-formatting to f-strings, `os.path` to `pathlib`, type annotations starting
  with the `Zettel` class and the `zdb` boundary. Ruff can do the first
  mechanically.
- Break up `zettel.py`: the 240-line `main()` mixes argument parsing, filename
  templating and file writing.

---

## Pull request #43

[Delete old files and implement Poetry project](https://github.com/ZettelGeist/zettelgeist/pull/43),
opened by Nicholas Synovic in September 2024: 113 files changed, 75 deleted,
+1,822 / −5,715, based on `master`, still mergeable, described as "no functional
changes."

**The recommendation is to harvest it, not merge it.** Roughly half of it is work
this roadmap wants and would otherwise have to redo; the other half would break
the release and relicense the project. Phase 1 takes the first half as separate
commits with attribution to the author, and the PR is then closed with a link to
this section.

*Done in Phase 1.* The deletions and the formatting pass were taken as
described. The community files were not — see Phase 1 above for why the idea
survived the harvest but the contents did not.

### Worth taking

- **The 75 deletions.** Almost exactly Phase 1's prune list, already done. Four
  exceptions to keep: the `mlb` example zettels (Phase 3 needs them as fixtures —
  move them, don't delete them), `docs/index.html` and `docs/.nojekyll` (together
  the live GitHub Pages redirect to the wiki), and `docs/RELEASING.md`. Note that
  `.nojekyll` and `setup.cfg` appear in the PR as *renames* into
  `.github/CODE_OF_CONDUCT.md` and `.github/CONTRIBUTING.md` — GitHub matched two
  empty files against two new ones, so the deletion is easy to miss.
- **The formatting pass.** All seven modules were tokenized at the PR head
  against `master`: the only differences are import order, trailing commas, quote
  style, one de-duplicated `pprint` import, and trailing whitespace inside the
  grammar string. The "no functional changes" claim holds for the Python modules.
  The `try/except ImportError` around the libyaml C loader survives isort intact.
- **The community files** — `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`,
  `SECURITY.md`, `SUPPORT.md`, `GOVERNANCE.md`, `CITATION.cff`, the devcontainer,
  and `.pre-commit-config.yaml` to keep the formatting from drifting back.

### Not worth taking

- **It relicenses the project.** `LICENSE` is replaced wholesale with the AGPL
  v3, and the new `pyproject.toml` declares `license = "GNU Affero"` while its own
  classifiers still say Apache 2.0. That is a decision for the copyright holders
  and deserves a separate PR.
- **The packaging does not package ZettelGeist.** `[tool.poetry] name = "src"`,
  version 0.1.0, and the only source directory it declares is a new `src/`
  holding an empty `main.py` stub. The real `zettelgeist/` package is not
  included, and `setup.py` — which carries the four `console_scripts` — is
  deleted. Build and install the result and no `zettel`, `zimport`, `zfind` or
  `zcreate` command exists.
- **The dependencies are gone.** The Poetry file declares only `python` and
  `pytest` — the latter as a runtime dependency. `python-frontmatter` and `tatsu`
  are not listed.
- **It deletes the test suite** and leaves a `tests/.gitkeep` behind. Phase 2
  depends on repairing those tests, not replacing them with nothing.
- **It replaces the README** with the unedited "Python Template Repository"
  boilerplate.

### Sequencing

PR #43 branches from `master` as it stood before Phase 0, so it does not contain
the four `dev` commits — and it reformats `zettel.py` and `zimport.py`, the two
files those commits change. Phase 0 having landed first, Phase 1 should re-run
the formatter on the merged result rather than taking the PR's version of those
two files. Doing it the other way means resolving conflicts between a bug fix and
a reformat, which should be avoided if possible.

---

## Where each open issue lands

| # | Issue | Phase | Status after the plan |
|---|-------|-------|-----------------------|
| 42 | `counter` does not default to `id` | 0 ✅ | Fixed in 1.1.6 |
| 39 | Allow Unicode in `yaml.dump` | 0 ✅ | Fixed in 1.1.6 |
| 37 | Use YAML not JSON for `.counter.dat` | 0 ✅ | Fixed in 1.1.6 |
| 38 | Query grammar | 3 | Root cause found: two-char fix, then fts5 |
| 41 | Terminal output of `zimport` | 4 | Summary line landed in 1.1.6; verbosity levels remain |
| 33 | Config files for command options | 4 | New `zettelgeist init` and `.zettelgeist/` |
| 31 | Short forms for `zfind` arguments | 4 | Falls out of centralized argparse |
| 34 | Simplify `zfind` output options | 4 | `--show FIELD...`, old flags aliased |
| 35 | Unique identifier per zettel | 4 | UUID on create, backfill for existing notes |

---

## Before Phase 3: check the fixture corpus

With the grammar fixed, `tags:"National League"` still returns all 29 baseball
zettels — because in `tests/fixtures/mlb` (`deprecated/docs/example/mlb` when
this was written) every team, American League included, carries the tag
`National League`. The fixture data is wrong, not the
query. Issue 38 expects 15, so confirm which corpus the wiki tutorial actually
ships before writing that assertion into a test.

---

*Findings reproduced locally on Python 3.12.3, PyYAML 6.0.2, Tatsu 5.13.1.
Issues and PR #43 read from `ZettelGeist/zettelgeist`.*
