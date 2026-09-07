# AGENTS.md

Working notes for coding agents in this repository. Humans are welcome to read
it; nothing here is agent-specific except the tone.

Read [ROADMAP.md](ROADMAP.md) before proposing work. It says what is broken, in
what order it is being fixed, and why — most "obvious" cleanups in this tree are
already scheduled into a phase, and doing them out of order creates conflicts.

## What this project is

ZettelGeist is a plaintext note-taking system. Notes ("zettels") are YAML or
Markdown-with-frontmatter files; `zimport` indexes them into a SQLite
full-text-search database, and `zfind` queries that index through a small query
language (ZQL) defined as a Tatsu grammar in `zettelgeist/zdb.py`.

Four console scripts are declared in `setup.py`:

| Command | Module | Purpose |
|---------|--------|---------|
| `zettel` | `zettelgeist/zettel.py` | Create and edit a zettel |
| `zimport` | `zettelgeist/zimport.py` | Index a directory of zettels |
| `zfind` | `zettelgeist/zfind.py` | Query the index |
| `zcreate` | `zettelgeist/zcreate.py` | Deprecated; prints a notice and is retired in Phase 4 |

## Layout

```
zettelgeist/      the package — all real source lives here
tests/            one test module (currently broken, see below)
tests/fixtures/   the mlb corpus, moved here in Phase 1
docs/             NOT documentation — this is the GitHub Pages root
.github/          workflows and the community health files
bin/              four shell shims that duplicate the console_scripts
scripts/          deploy.sh, superseded by the release workflow
```

Phase 1 deleted the dead half of the tree — `deprecated/`, `sphinx-docs/`,
`project/`, `adhoc/`, `jupyter/`, `src/`, `zdb_funcs.sh` and `BETA.md`. What is
left outside `zettelgeist/`, `tests/` and `docs/` is `bin/` and `scripts/`,
both of which go in Phase 2 once the entry points and the release workflow are
settled. Don't invest in either, and don't delete them ad hoc either — that
phase has an order to it.

## Setup

```sh
python -m venv .venv && . .venv/bin/activate
pip install -e .
```

Both `venv/` and `.venv/` are in `.gitignore`.
Requires Python ≥ 3.10; developed against 3.12. Runtime dependencies are
`python-frontmatter` and `tatsu` — plus `PyYAML`, which every module imports but
which nothing declares (it arrives transitively through `frontmatter`). Phase 2
fixes that; until then, be aware the installed PyYAML version is unpinned.

## Tests

```sh
pip install pytest
python -m pytest
```

**The suite does not currently pass**, and this is known, not something to fix
opportunistically: `tests/test_zettelgeist.py` calls `yaml.load(doc)` with a
single argument, which PyYAML 6 removed. Repairing it is Phase 2 work, along with
adding pytest as a declared dev dependency and adding a CI job that runs it. If
you are working before Phase 2 lands, verify changes by exercising the commands
against `tests/fixtures/mlb` rather than by trusting a green run you did not
get.

There is no CI test job. The single workflow, `.github/workflows/release.yml`,
builds and publishes to PyPI on any tag push.

## Working conventions

- **Branch off `master`.** Use a short topic branch per unit of work
  (`roadmap`, `issue-38`, …). `dev` is the branch that tracks what is about to
  land; don't treat it as a catch-all.
- **Use [Conventional Commits](https://www.conventionalcommits.org/)** for
  commit subjects: `fix:`, `feat:`, `docs:`, `style:`, `refactor:`, `test:`,
  `chore:`. Say in the body what you verified and how.
- **Pull requests go to `ZettelGeist/zettelgeist`**, not to a fork. So do issues:
  `gh issue list --repo ZettelGeist/zettelgeist`. A bare `gh` command may default
  to a fork that has issues disabled.
- **Never push a tag.** Tagging publishes to PyPI — the release workflow fires on
  `refs/tags/*`. Releases follow `docs/RELEASING.md` and are the maintainers'
  call.
- **One phase at a time.** Phases in ROADMAP.md are ordered by dependency, and
  each is meant to end at a state that could be tagged.

## Style

The package is formatted with isort (`.isort.cfg`, profile=black) and Black at
its default line length, landed as a single pass in Phase 1. Keep it that way:

```sh
pip install pre-commit && pre-commit install
pre-commit run --all-files
```

There is no linter in the hooks yet, on purpose — flake8 and bandit both report
roughly a hundred findings against the legacy style, so either would be a gate
that is red on day one. `.pre-commit-config.yaml` says so at the top, and Phase
2 settles which linter this project runs.

Underneath the formatting, the code still predates most of the Python it runs
on: `%`-formatting throughout, no type annotations, `os.path` rather than
`pathlib`, bare `except:` clauses, and diagnostics printed straight to stdout.
Modernizing that is Phase 5, deliberately last and deliberately incremental.

Until then: write new code in the modern idiom — f-strings, `pathlib`,
annotations on anything new — but **do not modernize code you are not otherwise
changing.** A drive-by rewrite of a file makes the real diff unreviewable.

## Traps

- `docs/` is the GitHub Pages source (`master:/docs`, served at
  zettelgeist.org/zettelgeist). It contains a redirect to the wiki and a
  `.nojekyll`, not documentation. Adding a file there publishes it. Repository
  documentation goes at the root.
- The 29 baseball zettels under `tests/fixtures/mlb` are the corpus every
  issue-38 reproduction is stated against, and Phase 3 promotes them to a real
  pytest fixture with asserted counts. Their bytes are load-bearing: the
  whitespace-fixing pre-commit hooks are configured to skip `tests/fixtures/`
  for that reason. Read `tests/fixtures/README.md` before changing any of them —
  the corpus has a known defect that the roadmap asks to be settled first.
- `zettelgeist/zdb.py` holds the ZQL grammar as a plain (non-raw) string
  containing `\s`. It emits a `SyntaxWarning` on 3.12. Editing that string is
  delicate: a compiled-SQL regression test is the only thing that catches a
  mistake, and there is no such test until Phase 3. (Trailing whitespace inside
  it turned out not to matter — Phase 1 stripped two trailing spaces and
  verified the compiled ASTs were unchanged — but the rest of the whitespace is
  significant to the parse.)
- `zutils.md5_for_file()` raises `NameError`; `hashlib` is never imported. It is
  a known latent bug, not a symptom of something you just broke.
- `bin/` duplicates the console scripts. If a command behaves oddly, check which
  one is on `PATH`.
- Three latent crashes found while writing the Phase 1 README, none of them in
  the issue tracker and all of them Phase 5 work: `zettel --file` on a note with
  an unknown field prints the right diagnostic and then dies with an
  `UnboundLocalError`; `zfind --publish` raises `TypeError` on any note carrying
  a `cite` field unless `--publish-conf` is also given; and `zimport --validate`
  creates the database file even though it indexes nothing.
