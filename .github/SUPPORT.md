# Getting help with ZettelGeist

## Documentation

The [wiki](https://github.com/ZettelGeist/zettelgeist/wiki) is the
documentation: installation, the tutorial, and the ZQL query language. It is
also what zettelgeist.org/zettelgeist redirects to.

The [README](../README.md) covers installation and a short tour of the four
commands. Every command takes `--help`.

## Questions

Open an [issue](https://github.com/ZettelGeist/zettelgeist/issues) and say what
you were trying to do. Questions are welcome there; there is no separate forum.

Useful things to include:

- the exact command line, and the output you got
- the ZettelGeist version (`python -c "from zettelgeist import zversion;
  print(zversion.version())"`)
- your Python version
- for a search problem, the compiled SQL:
  `python -c "from zettelgeist import zquery; print(zquery.compile(YOUR_QUERY)[0])"`

## Known rough edges

Before filing, it may save you time to know that these are already understood
and scheduled in [ROADMAP.md](../ROADMAP.md):

- **Quoted phrases in queries match on the last word only.** `tags:"AL Central"`
  searches for `Central`. Issue 38; fixed in Phase 3.
- **`zcreate` is deprecated.** Use `zimport --create`. It prints a notice saying
  so on every run.
- **The commands take a lot of typing**, and `--database` is required every
  time. A config file and short flags are Phase 4.
- **`zutils.md5_for_file()` raises `NameError`.** It is unused by the commands;
  Phase 5 fixes it.

## Reporting a vulnerability

Not through issues — see [SECURITY.md](SECURITY.md).
