# Security policy

## Supported versions

ZettelGeist is a small project maintained by a handful of people. Only the
latest release on [PyPI](https://pypi.org/project/zettelgeist/) is supported;
fixes are made on `master` and released from there.

| Version | Supported |
|---------|-----------|
| 1.1.x   | ✅        |
| < 1.1   | ❌        |

## Reporting a vulnerability

**Do not open a public issue.** Use one of:

- GitHub's [private vulnerability
  reporting](https://github.com/ZettelGeist/zettelgeist/security/advisories/new)
  on this repository, or
- email George K. Thiruvathukal at <gkt@cs.luc.edu>.

Please include what you found, how to reproduce it, and what an attacker could
do with it. You should get an acknowledgement within a week or so; this is not a
funded project with an on-call rotation, so please be patient with the timeline
and let us know if you have a disclosure deadline.

## Scope, honestly stated

ZettelGeist is a local command-line tool. It reads YAML and Markdown files you
point it at, writes a SQLite index, and prints results. It opens no sockets,
runs no server, and has no authentication or multi-user model. The realistic
threat is a malicious note file rather than a remote attacker.

Things that are in scope:

- Anything that makes `zimport` or `zfind` execute code, write outside the paths
  it was given, or read files it was not pointed at, when given a hostile
  `.yaml` or `.md` file.
- SQL injection through a ZQL query or through indexed note content. The
  generated SQL is assembled by string interpolation in `zettelgeist/zquery.py`,
  which is a real weak point and is being reworked in Phase 3 of
  [ROADMAP.md](../ROADMAP.md).
- Anything that lets the `--publish` template mechanism in `zfind` reach outside
  formatting.

Things that are **not** vulnerabilities in this tool:

- Static-analysis findings on their own. Bandit reports the SQL string building
  above and the MD5 checksum in `zutils.md5_for_file()`; the first is known and
  scheduled, and the second is a file digest, not a security hash. A report
  saying only "bandit flags this" will be closed with a pointer here.
- Bugs that require you to already be able to write files the tool reads and run
  commands as the user. That is the tool's entire operating model.
