# ZettelGeist

[![Build Status](https://www.travis-ci.org/ZettelGeist/zettelgeist.svg?branch=master)](https://www.travis-ci.org/ZettelGeist/zettelgeist)
# Overview

ZettelGeist is yet-another notetaking system. Details of this work in progress can be found on our wiki.

Unlike other notetaking systems, our system starts with an information model. GUI and web clients are not going to be developed until we are
confident about the information model.

We start with the assumption that notetaking is both a personal and a collaborative activity.

One must always be able to write notes *offline* and store them in a shared folder (e.g. Dropbox) or hosted version conrtrol system, such as Git.

Rather than build yet another proprietary format, our notes are designed using YAML and will be indexed using a full-text indexing capable database.
We're working with Python + sqlite3, but we are completely agnostic and could just as easily support Java/Scala + H2 in the future. We're certainly
interested in having others replicate our approach but also welcome anyone to the team who wants to partipcate.

# Current Tools

- zcreate: Creates the database (uber simple)
- zimport: Imports a folder of YAML notes into the database (not incremental yet but soon will be)
- zfind: Searches the database fields using sqlite3's full-text search engine (FTS4 presently)
- zreplace: Under development

- create_random_zettels: A script to generate a large number of random text files for indexing purposes.

See the wiki for details about our requirements and basic design.

# Notes

How to get unique tags/mentions after running zimport:

```
sqlite3 yourdatabase.db 'select distinct(tag) from tags' | sort -f | uniq -i 
sqlite3 yourdatabase.db 'select distinct(mention) from mentions' | sort -f | uniq -i
```

These will become two command line tools soon.
