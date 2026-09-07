# Contributing to ZettelGeist

Thanks for your interest. This is a small project with a small readership, so
the process is light — but it does have an order to it, and following that order
saves everyone rework.

## Read the plan first

[ROADMAP.md](../ROADMAP.md) says what is broken, in what order it is being
fixed, and why. Most of the obvious cleanups in this tree are already scheduled
into a phase, and doing one out of order creates conflicts with work that is
already queued. If you are about to send a change that isn't a bug fix, check
the roadmap for where it lands.

[AGENTS.md](../AGENTS.md) is the same material aimed at coding agents, and it
carries the traps — the parts of this codebase that will bite you. Humans should
read it too.

## Setting up

```sh
python -m venv .venv && . .venv/bin/activate
pip install -e .
```

Requires Python 3.10 or newer; development happens on 3.12. The four commands —
`zettel`, `zimport`, `zfind`, `zcreate` — are installed as console scripts.

## Tests

```sh
pip install pytest
python -m pytest
```

**The suite does not currently pass.** `tests/test_zettelgeist.py` calls
`yaml.load(doc)` with one argument, which PyYAML 6 removed. This is known, and
repairing it is Phase 2 work rather than something to fix in passing. Until then,
verify a change by exercising the commands against `tests/fixtures/mlb` rather
than by trusting a green run you did not get.

## Formatting

The package is formatted with [isort](https://pycqa.github.io/isort/) (settings
in `.isort.cfg`) and [Black](https://black.readthedocs.io/) at its default line
length. Install the hooks once and it happens on its own:

```sh
pip install pre-commit
pre-commit install
```

To check the whole tree, `pre-commit run --all-files`.

There is deliberately no linter in the hooks yet — see the comment at the top of
`.pre-commit-config.yaml` for why, and ROADMAP.md Phase 2 for when.

**Do not reformat or modernize code you are not otherwise changing.** A drive-by
reformat makes the real diff unreviewable. Write new code in the modern idiom —
f-strings, `pathlib`, type annotations — and leave the surrounding legacy alone;
modernizing it is Phase 5, deliberately incremental.

## Pull requests

- **Branch off `master`**, one short topic branch per unit of work (`issue-38`,
  `phase-2-packaging`). `dev` tracks what is about to land; it is not a
  catch-all.
- **Open the pull request against `ZettelGeist/zettelgeist`**, not against a
  fork. Issues live there too — a bare `gh` command may default to a fork that
  has issues disabled, so pass `--repo ZettelGeist/zettelgeist`.
- **Use [Conventional Commits](https://www.conventionalcommits.org/)** for
  commit subjects: `fix:`, `feat:`, `docs:`, `style:`, `refactor:`, `test:`,
  `chore:`. Say in the body what you verified and how.
- **Never push a tag.** A tag publishes to PyPI — the release workflow fires on
  `refs/tags/*`. Releases follow [docs/RELEASING.md](../docs/RELEASING.md) and
  are the maintainers' call.

## What goes where

```
zettelgeist/      the package — all real source lives here
tests/            the suite, plus tests/fixtures/mlb, the baseball corpus
docs/             NOT documentation — this is the GitHub Pages root
```

`docs/` holds a redirect to the wiki and a `.nojekyll`. Adding a file there
publishes it to zettelgeist.org/zettelgeist. Repository documentation goes at the
root; user documentation goes in the
[wiki](https://github.com/ZettelGeist/zettelgeist/wiki).

## Reporting a bug

Open an issue at
[ZettelGeist/zettelgeist/issues](https://github.com/ZettelGeist/zettelgeist/issues)
with the command you ran, what you expected, and what you got. If it involves
search, the compiled SQL is the useful detail:

```python
from zettelgeist import zquery
print(zquery.compile('tags:"AL Central"')[0])
```

For anything security-related, see [SECURITY.md](SECURITY.md) instead.
