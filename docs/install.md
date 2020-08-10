---
layout: page
title: Installation
permalink: /install/
---

## Prerequisites for All Installations

We support Unix/Linux, OS X using [Homebrew](https://brew.sh/), and Windows using [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install-win10).

Python 3 is required. We do not yet support multiple versions of Python.

We recommend installing [bibutils](https://sourceforge.net/p/bibutils/home/Bibutils/) and 
[sqlite3 with full-text search](https://www.sqlite.org/fts3.html). 
Neither is required, but we may ask you to share output from sqlite3 commands with us in bug reports.

Please note that ZettelGeist is a command line application built for people who prefer working with the command line, plaintext, and text editors.
If this is not you, you will probably not like ZettelGeist.

## Installation for General Users

1. Create a virtual environment for running ZettelGeist:

   ```shell
   $ python3 -m venv ~/zenv
   ```

   You may install your environment wherever you like.
   We will assume `~/zenv`.

2. Source the virtual environment

   ```shell
   $ . ~/zenv/bin/activate
   ```

   The prompt will now be prefixed by `(zenv)`, the environment created in (1).

3. Confirm that you are picking up the right `python` and `pip`.

   ```shell
   (zenv) $ which pip
   /path/to/zenv/bin/pip
   (zenv) $ which python
   /path/to/zenv/bin/python
   ```

  In place of `path/to/` you should see the absolute path to the environment created in (1). 

4. Install ZettelGeist

   ```shell
   (zenv) $ pip install zettelgeist
   Collecting zettelgeist
     Downloading zettelgeist-0.12.2-py3-none-any.whl
   Collecting tatsu (from zettelgeist)
     Using cached TatSu-4.2.5-py2.py3-none-any.whl
   Collecting PyYAML (from zettelgeist)
   Installing collected packages: tatsu, PyYAML, zettelgeist
   Successfully installed PyYAML-3.12 tatsu-4.2.5 zettelgeist-0.12.2
   ```
 
   If you see `zettelgeist-<version>` in the output, you should have a successful install. 

5. Verify the installation

   ```shell
   (zenv) $ which zcreate
   /path/to/zenv/bin/zcreate
   (zenv) $ which zimport
   /path/to/zenv/bin/zimport
   (zenv) $ which zfind
   /path/to/zenv/bin/zfind
   (zenv) $ which zfilter
   /path/to/zenv/bin/zfilter
   (zenv) $ which zettel
   /path/to/zenv/bin/zettel
   ```

You may now proceed to the page [Getting Started](/gs).

To return to the system environment execute `deactivate`:

```
(zenv) $ deactivate
```

<!--
## Developer Install

Coming soon.
-->