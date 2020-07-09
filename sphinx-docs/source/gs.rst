Getting Started
===================


Prerequisites
-------------

Please visit the `Installation </install>`__ before starting the
tutorial. This tutorial assumes you have installed ZettelGeist and have
confirmed that the tools are available in a Python virtualenv.

We assume that your virtualenv is named ``zenv`` here. Wherever you see
``zenv`` here, your setup can be different, as long as you completed the
installation and verified that it is nominally functioning.

This tutorial also depends on sample files, provided at
https://github.com/ZettelGeist/zg-tutorial. You can visit this page to
download the examples, or you can use ``git`` to fetch it:

.. code:: shell

   $ git clone https://github.com/ZettelGeist/zg-tutorial.git

This will create the folder ``zg-tutorial``, which we’ll reference in
this tutorial.

Creating Zettels
----------------

The ``zettel`` command is used to create zettels. You can also create
zettels using an ordinary text editor.

Getting help
~~~~~~~~~~~~

.. code:: shell

   zettel --help

The help shows what at first glance appears to be a bewildering number
of options. However, most of the options are *the same* and are just
being used to do an operation (set, delete, append, etc.) on any given
field.

Create a simple zettel
~~~~~~~~~~~~~~~~~~~~~~

.. code:: shell

   zettel --set-title "My First Zettel"

This results in the following output:

.. code:: yaml

   title: My First Zettel

Create zettel with multiple fields
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A zettel can have as few fields as you wish, including zero. However, a
zettel only becomes interesting as you add more information. Let’s add a
*summary* and a *note*.

.. code:: shell

   zettel --set-title "My First Zettel" --set-summary "A Zettel with a note" --set-note "Line 1\nLine 2\nLine 3"

This results in

.. code:: yaml

   title: My First Zettel
   summary: A Zettel with a note
   note: |-
     Line 1
     Line 2
     Line 3

When setting a field to a string value as we have done for each of these
fields, it is permitted to have *embedded newlines* anywhere you like.
For the note we have written, we have three input lines, each of which
appears on a separate line.

YAML (the format in which Zettels are stored) provides excellent support
for this concept and will take your text and indent it using a multiline
string. As long as each line is indented consistently relative to the
*note* key, it will be valid.

Obviously, writing longer strings using the command line is sometimes
impractical, so we created two ways of being able to do this easily:
prompting for input (using the ``--prompt-<FIELD>`` options) or by
loading the plaintext from a file (using ``--load-<FIELD>``). Each of
these is easy to demonstrate.

Let’s try loading some text by having ``zettel`` prompt for it. We’ll
modify the above command as follows:

.. code:: shell

   zettel --set-title "My First Zettel" --set-summary "A Zettel with a note" --prompt-note

::

   Enter text for note. ctrl-d to end.
   note> Line 1
   note> Line 2
   note> Line 3
   note>
   note> Even a blank line is allowed.
   note>

Results

.. code:: yaml

   title: My First Zettel
   summary: A Zettel with a note
   note: |-
     Line 1
     Line 2
     Line 3

     Even a blank line is allowed.

Load field from another file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TODO

Indexing Zettels for Search
---------------------------

For this section, we provide you with access to some sample zettels.
These can be found in the ZettelGeist tutorial repository at
https://github.com/ZettelGeist/zg-tutorial.git. (See Prerequisites
above.)

You can be in any folder while trying this, but we’ll assume you are in
the ``zettelgeist\docs`` after performing an initial clone of our
repository.

.. code:: shell

   $ cd zg-tutorial
   $ zcreate --database mlb.db
   Creating new database mlb.db


.. code:: shell

   $ ls zettels/baseball

   arizona-diamondbacks.yaml  milwaukee-brewers.yaml
   atlanta-braves.yaml        minnesota-twins.yaml
   baltimore-orioles.yaml     new-york-mets.yaml
   boston-red-sox.yaml        new-york-yankees.yaml
   chicago-cubs.yaml          oakland-athletics.yaml
   chicago-grey-sox.yaml      philadelphia-phillies.yaml
   cincinnati-reds.yaml       pittsburgh-pirates.yaml
   cleveland-indians.yaml     san-diego-padres.yaml
   colorado-rockies.yaml      seattle-mariners.yaml
   detroit-tigers.yaml        st-louis-cardinals.yaml
   houston-astros.yaml        tampa-bay-rays.yaml
   kansas-city-royals.yaml    texas-rangers.yaml
   los-angeles-angels.yaml    toronto-blue-jays.yaml
   los-angeles-dodgers.yaml   washington-nationals.yaml
   miami-marlins.yaml```


.. code:: shell

   $ zimport --database mlb.db --dir $(pwd)

   Importing /Users/gkt/Work/zg-tutorial/zettels/baseball/baltimore-orioles.yaml
   Importing /Users/gkt/Work/zg-tutorial/zettels/baseball/kansas-city-royals.yaml
   Importing /Users/gkt/Work/zg-tutorial/zettels/baseball/los-angeles-angels.yaml
   Importing /Users/gkt/Work/zg-tutorial/zettels/baseball/miami-marlins.yaml
   Importing /Users/gkt/Work/zg-tutorial/zettels/baseball/milwaukee-brewers.yaml
   Importing /Users/gkt/Work/zg-tutorial/zettels/baseball/seattle-mariners.yaml
   Importing /Users/gkt/Work/zg-tutorial/zettels/baseball/arizona-diamondbacks.yaml
   Importing /Users/gkt/Work/zg-tutorial/zettels/baseball/st-louis-cardinals.yaml
   Importing /Users/gkt/Work/zg-tutorial/zettels/baseball/houston-astros.yaml
   Importing /Users/gkt/Work/zg-tutorial/zettels/baseball/oakland-athletics.yaml
   Importing /Users/gkt/Work/zg-tutorial/zettels/baseball/boston-red-sox.yaml
   Importing /Users/gkt/Work/zg-tutorial/zettels/baseball/new-york-yankees.yaml
   Importing /Users/gkt/Work/zg-tutorial/zettels/baseball/pittsburgh-pirates.yaml
   Importing /Users/gkt/Work/zg-tutorial/zettels/baseball/detroit-tigers.yaml
   Importing /Users/gkt/Work/zg-tutorial/zettels/baseball/cincinnati-reds.yaml
   [...]

What you see will differ slightly. Where you see ``/Users/gkt/Work``,
you are likely to see the path to your own checkout directory.

Let’s look at one of these zettels.

.. code:: yaml

   title: MLB Teams
   summary: Arizona Diamondbacks
   note: |
     The Arizona Diamondbacks, often shortened as the D-backs, are an American professional
     baseball franchise based in Phoenix, Arizona. The club competes in Major League
     Baseball (MLB) as a member of the National League (NL) West division. Since the
     team's inception in 1998, the franchise has played home games at Chase Field, formerly
     known as Bank One Ballpark. The Diamondbacks have won one World Series championship
     (in 2001), becoming the fastest expansion team in the Major Leagues to win a championship,
     doing it in only the fourth season since the franchise's inception in the 1998 Major
     League Baseball season.
   tags:
   - MLB
   - National League
   - NL West
   cite:
     bibkey: arizona-diamondbacks-wikipedia
     page: web page

Each of these zettels contains some information one might typically
place on a note card. In our view of the world, notes would include
important basics. The note will often be one of the longer fields. It
can be written using what is known as the YAML block style. This means
that all lines of input are taken, provided they maintain the same
indentation level and/or blank. Everything will be taken as input until
the next field or end of file is found.

Also shown here are how you can maintain a list of tags. The ``tags``
field allows you to specify one or more tags. While we hope one day to
build an auto-classifier (someday, someday…), we find that we actually
need to assign labels, especially in our own book project that is
actually making use of these tools.

Search Examples
---------------

Searching is done (at present) using the ``zfind`` tool. This tool can
only perform AND-style queries, but it will soon offer every conceivable
possibility. This limitation is similar to what you find in systems like
Gmail’s search operators, but even Gmail allows for NOT terms.

The ``zfind`` tool has options to search every field. Once a field
matches, you can use the show options to project values from the Zettel.
There is also a ``--count`` option to tell you how many Zettels matched
a query.

Find how many Zettels mention Chicago in the ``summary`` field:

::

   zfind --database mlb.db --find-summary Chicago --count
   2 Zettels matched search

…and print the ``summary and``\ filename\` of the zettels:

::

   zfind --database mlb.db --find-summary Chicago --count --show-filename
   filename:
   20170731132024-chicago-cubs.yaml

   ----------------------------------------

   filename:
   20170731155613-chicago-grey-sox.yaml

   ----------------------------------------

   2 Zettels matched search

…and show the ``summary`` about the teams:

::

   zfind --database mlb.db --find-summary Chicago --count --show-filename --show-summary
   summary:
   Chicago Cubs

   filename:
   20170731132024-chicago-cubs.yaml

   ----------------------------------------

   summary:
   Chicago White Sox

   filename:
   20170731155613-chicago-grey-sox.yaml

   ----------------------------------------

Find the terms MLB and Central in the ``note`` field. Upon finding a
match, show the ``filename`` and the ``summary`` fields.

::

   zfind --database mlb.db --find-note "MLB Central" --show-filename --show-summary
   summary:
   Chicago Cubs

   filename:
   20170731132024-chicago-cubs.yaml

   ----------------------------------------

   summary:
   Cincinnati Reds

   filename:
   20170731133642-cincinnati-reds.yaml

   ----------------------------------------

   summary:
   Pittsburgh Pirates

   filename:
   20170731135121-pittsburgh-pirates.yaml

   ----------------------------------------

   summary:
   St. Louis Cardinals

   filename:
   20170731135823-st-louis-cardinals.yaml

   ----------------------------------------

Find all zettels with Cubs mentioned in the ``note`` field:

::

   zfind --database mlb.db --find-note Cubs --show-note

   note:
   The Chicago Cubs are an American professional baseball team based in Chicago, Illinois. The Cubs compete in Major League Baseball (MLB) as a member club of the National League (NL) Central division, where they are the defending World Series champions. The team plays its home games at Wrigley Field, located on the city's North Side. The Cubs are one of two major league teams in Chicago; the other, the Chicago White Sox, is a member of the American League (AL) Central division. The Cubs, first known as the White Stockings, was a founding member of the NL in 1876, becoming the Chicago Cubs in 1903.[2] The Cubs have appeared in a total of eleven World Series. The 1906 Cubs won 116 games, finishing 116–36 and posting a modern-era record winning percentage of .763, before losing the World Series to the Chicago White Sox by four games to two. The Cubs won back-to-back World Series championships in 1907 and 1908, becoming the first major league team to play in three consecutive World Series, and the first to win it twice. Most recently, the Cubs won the 2016 National League Championship Series and 2016 World Series, which ended a 71-year National League pennant drought and a 108-year World Series championship drought,
