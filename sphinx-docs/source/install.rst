Prerequisites for All Installations
-----------------------------------

Python 3 is *required* to use ZettelGeist. We don’t have resources to
support multiple versions of Python.

We also recommend installing
`bibutils <https://sourceforge.net/p/bibutils/home/Bibutils/>`__ and
`sqlite3 with full-text search <https://www.sqlite.org/fts3.html>`__.
You may not need either of these, but should you run into issues, we may
ask you to share some output from sqlite3 commands with us in your bug
reports.

We only support Unix/Linux, OS X using `Homebrew <https://brew.sh/>`__,
and Windows using `Windows Subsystem for
Linux <https://docs.microsoft.com/en-us/windows/wsl/install-win10>`__.

Please also note that ZettelGeist is not a web-based or GUI program
(yet). This system is for people who *prefer* working with plaintext,
text editors, and the command line. If this is not you, you will
probably not like ZettelGeist and should proceed at your own peril.

Installation for General Users
------------------------------

-  Create a virtual environment for running ZettelGeist:

   .. code:: shell

      python3 -m venv ~/zenv

   You can install your environment wherever you like, but we are going
   to assume ``~/zenv`` in the remaining discussion and in our tutorial
   to *avoid* having to talk about user-specific details.

-  Source the virtual environment

   .. code:: shell

      . ~/zenv/bin/activate

-  And *ensure* that you are picking up the right ``python`` and
   ``pip``.

   .. code:: shell

      ~ . ~/zenv/bin/activate
      (zenv) ~ which pip
      /Users/gkt/zenv/bin/pip
      (zenv) ~ which python
      /Users/gkt/zenv/bin/python

   Your username would likely appear above instead of *gkt*, unless you
   share my initials.

-  Now install ZettelGeist

   .. code:: shell

      (zenv) ~ pip install zettelgeist
      Collecting zettelgeist
        Downloading zettelgeist-0.12.2-py3-none-any.whl
      Collecting tatsu (from zettelgeist)
        Using cached TatSu-4.2.5-py2.py3-none-any.whl
      Collecting PyYAML (from zettelgeist)
      Installing collected packages: tatsu, PyYAML, zettelgeist
      Successfully installed PyYAML-3.12 tatsu-4.2.5 zettelgeist-0.12.2

   If you see ``zettelgeist-<version>`` in the above output, you should
   have a successful install. Let’s verify:

   .. code:: shell

      (zenv) ~ which zcreate
      /Users/gkt/zenv2/bin/zcreate
      (zenv) ~ which zimport
      /Users/gkt/zenv2/bin/zimport
      (zenv) ~ which zquicksearch
      /Users/gkt/zenv2/bin/zquicksearch
      (zenv) ~ which zfilter
      /Users/gkt/zenv2/bin/zfilter
      (zenv) ~ which zettel
      /Users/gkt/zenv2/bin/zettel

-  And create your first zettel:

   .. code:: shell

      zettel --set-title "My First Zettel" --set-summary "I feel empowered." --append-tags "Tutorial" "ZettelGeist" "Install"
      title: My First Zettel
      summary: I feel empowered.
      tags:
      - Tutorial
      - ZettelGeist
      - Install

-  Then you should proceed to the `Getting Started </gs>`__ page.

Developer Install
-----------------

Coming soon.
