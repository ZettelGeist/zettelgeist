# ZettelGeist

ZettelGeist is a plaintext, historiographically focused notetaking system,
inspired by the Zettelkasten approach and built for research notes that outlive
the software that made them.

A note — a *zettel* — is a YAML file, or a Markdown file with YAML frontmatter.
Nothing is stored in a proprietary format and nothing is stored anywhere but
your own directory. `zimport` indexes a directory of them into a SQLite
full-text-search database, and `zfind` queries that index through **ZQL**, a
small query language. The index is disposable by design: delete it and rebuild
it from the notes at any time.

- **Documentation:** the
  [wiki](https://github.com/ZettelGeist/zettelgeist/wiki)
- **Plan of record:** [ROADMAP.md](ROADMAP.md) — what is broken, in what order
  it is being fixed
- **Contributing:** [.github/CONTRIBUTING.md](.github/CONTRIBUTING.md)

## Status

Current release: **1.1.6**. Requires Python 3.10 or newer.

Continuous integration does not yet run the test suite — the only workflow
builds and publishes on a tag. Fixing that, along with declaring PyYAML as the
dependency it has always been, is
[Phase 2](ROADMAP.md#phase-2--make-the-build-tell-the-truth); a real build badge
goes here when there is a build to report on.

One known bug is worth knowing before you rely on search: **a quoted phrase in a
query matches on its last word only.** `tags:"AL Central"` searches for
`Central`, so it over-matches rather than failing loudly. This is
[issue 38](https://github.com/ZettelGeist/zettelgeist/issues/38), and
[Phase 3](ROADMAP.md#phase-3--fix-search) fixes it.

## Installing

```sh
pip install zettelgeist
```

Or from a checkout:

```sh
git clone https://github.com/ZettelGeist/zettelgeist.git
cd zettelgeist
python -m venv .venv && . .venv/bin/activate
pip install -e .
```

Either way you get four commands: `zettel`, `zimport`, `zfind`, and the
deprecated `zcreate`.

## What a zettel looks like

```yaml
title: Reading note
summary: Kant on judgment
tags:
- kant
- aesthetics
cite:
  bibkey: kant1790
  page: 12-18
note: |
  The third Critique treats judgment as the faculty that mediates between
  understanding and reason.
```

The fields are fixed, and `zettel` will refuse a file that uses others:

| Field | Type | |
|---|---|---|
| `title` `bibkey` `bibtex` `ris` `inline` `url` `summary` `comment` `note` | string | free text |
| `tags` `mentions` | list of strings | `tags` classify, `mentions` name people and places |
| `cite` | `bibkey` + `page` | a citation |
| `dates` | `year` + `era` | a date |

A `.md` zettel puts exactly this in YAML frontmatter between `---` markers and
keeps the prose below it; the prose is indexed as the `document` field.

## The commands

Every command takes `--help`, and each has a great many flags — reducing that is
[Phase 4](ROADMAP.md#phase-4--give-the-tools-a-workspace).

### `zettel` — write and check a zettel

With no output option it parses and prints to stdout, so it doubles as a
checker:

```sh
zettel --file notes/kant.yaml          # parse it and print it back
```

It reports the first problem it finds — `Invalid field bogus found in Zettel` —
and then exits non-zero with a traceback rather than a clean message. Tidying
that up is [Phase 5](ROADMAP.md#phase-5--modernize-the-source).

Build one from flags:

```sh
zettel --set-title "Reading note" \
       --set-summary "Kant on judgment" \
       --append-tags kant aesthetics \
       --set-cite kant1790 12-18
```

Write it to a generated filename with `--name`, which takes the components to
join — `id`, `timestamp`, `counter`:

```sh
zettel --set-title "Reading note" --name id timestamp --id kant
# writes kant-20260906202644.md

zettel --set-title "Second note"  --name id counter   --id kant
# writes kant-0001.md, and remembers the count in .counter.dat
```

Edit an existing one in place, keeping a backup:

```sh
zettel --file notes/kant.yaml --in-place --append-tags critique
```

`--prompt-FIELD` asks for a field interactively; `--load-FIELD` reads it from a
file; `--delete-FIELD` removes it.

### `zimport` — index a directory

```sh
zimport --database zettels.db --create --dir notes/
```

`--create` starts a fresh index, deleting any existing one; leave it off to add
to what is there. `--validate` parses every note and reports errors without
indexing any of them — though it still creates the database file if one is
missing. `--fullpath` stores absolute paths so the index resolves from anywhere.
It walks the directory recursively and takes `.yaml` and `.md`.

### `zfind` — query the index

```sh
zfind --database zettels.db --query-string 'tags:kant' --show-title --show-summary
```

Results print as YAML documents. Pick fields with `--show-FIELD`, or `--show-all`
for everything. Other useful modes:

```sh
zfind --database zettels.db --query-string 'tags:kant' --count
zfind --database zettels.db --get-all-tags          # every tag in the index
zfind --database zettels.db --get-all-mentions
zfind --database zettels.db --query-file q.zql --fileset matches.txt
zfind --database zettels.db --query-string 'tags:kant' --publish tmpl.txt
```

`--query-prompt` reads the query interactively instead. `--publish` renders each
result through a `%`-format template, which is how a search becomes a document;
if any matched note has a `cite` field, pass `--publish-conf` too, because
`--publish` alone raises a `TypeError` on those.

### `zcreate` — deprecated

Creates an empty database. `zimport --create` does the same thing; `zcreate`
prints a deprecation notice on every run and is retired in Phase 4.

## ZQL, the query language

A query is a field name, a colon, and what to look for:

```
tags:kant
summary:judgment
```

Combine them with `&` (and), `|` (or), `!` (and not), and parentheses:

```
tags:kant & tags:aesthetics
summary:Cubs | summary:Reds
tags:MLB ! tags:Central
(tags:MLB ! summary:Cubs) & tags:East
```

Quote a phrase with double quotes — `tags:"AL Central"` — but see the caveat in
[Status](#status) above: today that matches on `Central` alone. There is no
unary `not`; `!` is binary, and `a ! b` means "matches `a` and not `b`."

`zfind` compiles ZQL to SQL against the SQLite FTS table, and you can see what
it produced:

```python
>>> from zettelgeist import zquery
>>> print(zquery.compile('tags:kant & tags:aesthetics')[0])
SELECT * from (SELECT * FROM zettels WHERE zettels MATCH 'tags:kant'
INTERSECT SELECT * FROM zettels WHERE zettels MATCH 'tags:aesthetics')
```

## Try it

The repository ships a corpus of 29 notes, one per Major League Baseball team,
used as the test fixture:

```sh
zimport --database /tmp/mlb.db --create --dir tests/fixtures/mlb
zfind --database /tmp/mlb.db --query-string 'tags:"NL Central"' \
      --show-summary --show-tags --count
```

## Contributing

See [.github/CONTRIBUTING.md](.github/CONTRIBUTING.md). In short: read
[ROADMAP.md](ROADMAP.md) first, branch off `master`, open the pull request
against `ZettelGeist/zettelgeist`, and never push a tag — a tag publishes to
PyPI.

## License

Apache License 2.0. See [LICENSE](LICENSE).
