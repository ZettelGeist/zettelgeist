# Test fixtures

## `mlb/` — the baseball corpus

Twenty-nine zettels, one per Major League Baseball team, written in July 2017.
They previously lived at `deprecated/docs/example/mlb`, where they served as the
worked example for the tutorial that is now in the wiki. Phase 1 of
[ROADMAP.md](../../ROADMAP.md) moved them to `mlb/` ahead of deleting
`deprecated/`; Phase 3 promotes them to a real pytest fixture with asserted
result counts.

Every issue-38 reproduction in the roadmap is stated against this corpus, so the
files are load-bearing: change one and the counts recorded elsewhere stop
matching.

### Shape

Each file is pure YAML — no Markdown frontmatter — with `title`, `url`,
`summary`, `note` and `tags`. The `title` is `MLB Teams` in all 29; the team name
is in `summary`, and the `note` is a paragraph lifted from Wikipedia.

### Known defect in the data

**Every team carries the tag `National League`, American League teams included.**
This is wrong in the fixture, not in the query engine, and it is why
`tags:"National League"` returns 29 rather than the 15 that issue 38 expects.

Do not "fix" it casually. The counts in ROADMAP.md and in issue 38 were measured
against the corpus as it stands, and the wiki tutorial may ship a corrected
version of the same files; the roadmap's *Before Phase 3* section asks that this
be settled before any count is written into a test.

### Regenerating an index from it

```sh
zimport --database zettels.db --create --dir tests/fixtures/mlb
zfind --database zettels.db --query-string 'tags:"AL Central"' --count
```

This README lives here rather than in `mlb/` because `zimport` walks a
fixture directory for `.md` as well as `.yaml`, and a stray Markdown file
inflates its "Processed N files" line.
