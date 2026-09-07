# Governance

This file describes how ZettelGeist is actually run, so that a contributor can
tell who decides what without having to ask. It is short because the project is
small; it is written down because "small" is not the same as "arbitrary."

## Roles

**Maintainer.** George K. Thiruvathukal (<gkt@cs.luc.edu>) is the project lead
and copyright holder of record. He has the final say on scope, on what merges,
and on releases. Where this document and his decision differ, his decision is
the one that holds.

**Contributors.** Anyone who opens an issue or a pull request. No agreement to
sign and no commit history required.

There is no formal committer tier. Write access is granted case by case by the
maintainer.

## How decisions get made

By discussion in the open — in the issue or the pull request — and by
maintainer decision when discussion does not converge. Nothing is decided by
vote.

Changes of any size are expected to say what they change and why. Changes that
alter the shape of the project rather than fixing a bug are expected to argue
for themselves against [ROADMAP.md](../ROADMAP.md), which is the standing plan
of record: what is broken, in what order it is being fixed, and why that order.
Amending the roadmap is itself a pull request.

Three decisions are reserved to the copyright holders and will not be made
inside an ordinary pull request:

- **Relicensing.** The project is Apache 2.0. Changing that is not a
  housekeeping change and needs its own pull request and its own discussion.
  (A previous contribution proposed swapping in the AGPL as part of an unrelated
  cleanup; it was not taken, for this reason.)
- **Renaming or moving the project**, including the PyPI name.
- **Publishing a release.** See below.

## Merging

Pull requests go to `ZettelGeist/zettelgeist` and target `master`. A pull request
needs one approving review from the maintainer, or from someone the maintainer
has asked to review it. Authors do not merge their own pull requests without
that review.

Small and mechanical changes — a typo, a deletion of something already agreed
dead — can be merged on a single approval without further discussion. Anything
that changes behavior a user can see is expected to say so in its description
and to name the version it should land in.

## Releases

Releases are the maintainer's call. The procedure is
[docs/RELEASING.md](../docs/RELEASING.md).

**Contributors must never push a tag.** The release workflow fires on
`refs/tags/*` and publishes to PyPI; a tag pushed by accident is a publication,
not a bookmark.

## Changing this document

Open a pull request. It needs the maintainer's approval, like everything else.
