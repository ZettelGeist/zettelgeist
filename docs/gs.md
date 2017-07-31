---
layout: page
title: Getting Started
permalink: /gs/
---

ZettelGeist is only a few days old at the time of writing and is thus a work in progress. We're certainly excited about the direction in which the work is heading but at the same time don't want to commit to the interfaces you see here. At least until release (expected mid-summer) you should assume that many aspects of the interface and internals might change.

Owing to the nature of our work, where we are often keeping some proprietary materials in actual Zettels (that is, our notes), we cannot provide actual data files for you at this time. You most certainly can write your own notes based on literature you might be reviewing for your own scholarly project but we cannot provide any of our data sets (yet).

Luckily, we have a script that can *generate* some test data for you. The instructions here assume you have done a checkout or download of the ZettelGeist system and installed any needed dependencies. That is covered on our Installation page (or will be soon).

## Create some Zettels

Zettels can be created with a plaintext editor or the `zettel` command-line tool. I prefer the command-line tool at this stage, because it provides great insight into what goes into a Zettel.

You can start by getting help:

```shell
zettel --help
```

The help shows what at first glance appears to be a bewildering number of options. However, most of the options are *the same*. 

Let's start a simple example. We'll create a zettel on *standard output* that has nothing more than a title:

```
zettel --set-title "My First Zettel"
```

This results in the following output:

```yaml
title: My First Zettel
```

A zettel can have as few fields as you wish, including zero. However, a zettel only becomes interesting as you add more information. Let's add a *summary* and a *note*.

```shell
zettel --set-title "My First Zettel" --set-summary "A Zettel with a note" --set-note "Line 1\nLine 2\nLine 3"
```

This results in

```yaml
title: My First Zettel
summary: A Zettel with a note
note: |-
  Line 1
  Line 2
  Line 3
```

When setting a field to a string value as we have done for each of these fields, it is permitted to have *embedded newlines* anywhere you like. For the note we have written, we have three input lines, each of which appears on a separate line.

YAML (the format in which Zettels are stored) provides excellent support for this concept and will take your text and indent it using a multiline string. As long as each line is indented consistently relative to the *note* key, it will be valid.

Obviously, writing longer strings using the command line is sometimes impractical, so we created two ways of being able to do this easily: prompting for input (using the `--prompt-<FIELD>` options) or by loading the plaintext from a file (using `--load-<FIELD>`). Each of these is easy to demonstrate.

Let's try loading some text by having `zettel` prompt for it. We'll modify the above command as follows:

```shell
zettel --set-title "My First Zettel" --set-summary "A Zettel with a note" --prompt-note
```

```
Enter text for note. ctrl-d to end.
note> Line 1
note> Line 2
note> Line 3
note>
note> Even a blank line is allowed.
note>
```

Results

```yaml
title: My First Zettel
summary: A Zettel with a note
note: |-
  Line 1
  Line 2
  Line 3

  Even a blank line is allowed.
```







## Indexing Zettels for Search

For this section, we provide you with access to some sample zettels. These can be found in `docs/example/mlb`.

You can be in any folder while trying this, but we'll assume you are in the `zettelgeist\docs` after performing an initial clone of our repository.

```shell
$ cd zettelgeist/docs
$ zcreate --database mlb.db
Creating new database mlb.db
```

Let's take a look at the `example/mlb` folder:

```shell
$ ls example/mlb
20170731132024-chicago-cubs.yaml
20170731133642-cincinnati-reds.yaml
20170731134823-milwaukee-brewers.yaml
20170731135121-pittsburgh-pirates.yaml
20170731135823-st-louis-cardinals.yaml
20170731140433-atlanta-braves.yaml
20170731140750-miami-marlins.yaml
20170731141025-new-york-mets.yaml
20170731141248-philadelphia-phillies.yaml
20170731141625-washington-nationals.yaml
20170731141908-arizona-diamondbacks.yaml
20170731142237-colorado-rockies.yaml
20170731143033-los-angeles-dodgers.yaml
20170731143425-san-diego-padres.yaml
20170731154135-baltimore-orioles.yaml
20170731154404-boston-red-sox.yaml
20170731154645-new-york-yankees.yaml
20170731154837-tampa-bay-rays.yaml
20170731155132-toronto-blue-jays.yaml
20170731155613-chicago-grey-sox.yaml
20170731160002-cleveland-indians.yaml
20170731160508-detroit-tigers.yaml
20170731160722-kansas-city-royals.yaml
20170731160940-minnesota-twins.yaml
20170731161550-houston-astros.yaml
20170731161927-los-angeles-angels.yaml
20170731162502-oakland-athletics.yaml
20170731162806-seattle-mariners.yaml
20170731163040-texas-rangers.yaml
```

You may see more files than what is shown here. It's ok!

Let's import these files for indexing purposes:

```shell
zimport --database mlb.db --zettel-dir example/mlb
Importing 20170731132024-chicago-cubs.yaml
Importing 20170731133642-cincinnati-reds.yaml
Importing 20170731134823-milwaukee-brewers.yaml
Importing 20170731135121-pittsburgh-pirates.yaml
Importing 20170731135823-st-louis-cardinals.yaml
Importing 20170731140433-atlanta-braves.yaml
Importing 20170731140750-miami-marlins.yaml
Importing 20170731141025-new-york-mets.yaml
Importing 20170731141248-philadelphia-phillies.yaml
Importing 20170731141625-washington-nationals.yaml
Importing 20170731141908-arizona-diamondbacks.yaml
Importing 20170731142237-colorado-rockies.yaml
Importing 20170731143033-los-angeles-dodgers.yaml
Importing 20170731143425-san-diego-padres.yaml
Importing 20170731154135-baltimore-orioles.yaml
Importing 20170731154404-boston-red-sox.yaml
Importing 20170731154645-new-york-yankees.yaml
Importing 20170731154837-tampa-bay-rays.yaml
Importing 20170731155132-toronto-blue-jays.yaml
Importing 20170731155613-chicago-grey-sox.yaml
Importing 20170731160002-cleveland-indians.yaml
Importing 20170731160508-detroit-tigers.yaml
Importing 20170731160722-kansas-city-royals.yaml
Importing 20170731160940-minnesota-twins.yaml
Importing 20170731161550-houston-astros.yaml
Importing 20170731161927-los-angeles-angels.yaml
Importing 20170731162502-oakland-athletics.yaml
Importing 20170731162806-seattle-mariners.yaml
Importing 20170731163040-texas-rangers.yaml
Ignoring README.md; add .yaml extension to import this file.
```

Upon successful import of a file, you'll see only the line of output with Importing and nothing else.
This means that the file was imported into the index successfully.

Let's take a look at one of these files, `example/mlb/20170731132024-chicago-cubs.yaml`.

```yaml
title: MLB Teams
url: https://en.wikipedia.org/wiki/Chicago_Cubs
summary: Chicago Cubs
note: "The Chicago Cubs are an American professional baseball team based in Chicago,\
  \ Illinois. The Cubs compete in Major League Baseball (MLB) as a member club of\
  \ the National League (NL) Central division, where they are the defending World\
  \ Series champions. The team plays its home games at Wrigley Field, located on the\
  \ city's North Side. The Cubs are one of two major league teams in Chicago; the\
  \ other, the Chicago White Sox, is a member of the American League (AL) Central\
  \ division. The Cubs, first known as the White Stockings, was a founding member\
  \ of the NL in 1876, becoming the Chicago Cubs in 1903.[2] The Cubs have appeared\
  \ in a total of eleven World Series. The 1906 Cubs won 116 games, finishing 116\u2013\
  36 and posting a modern-era record winning percentage of .763, before losing the\
  \ World Series to the Chicago White Sox by four games to two. The Cubs won back-to-back\
  \ World Series championships in 1907 and 1908, becoming the first major league team\
  \ to play in three consecutive World Series, and the first to win it twice. Most\
  \ recently, the Cubs won the 2016 National League Championship Series and 2016 World\
  \ Series, which ended a 71-year National League pennant drought and a 108-year World\
  \ Series championship drought,"
tags:
- MLB
- National League
- NL East
```

Each of these has title, url, summary, and tags field. We're going to use these in some of the
search examples below.

## Search Examples

Searching is done (at present) using the `zfind` tool. This tool can only perform AND-style queries, but it will soon offer every conceivable possibility. This limitation is similar to what you find in systems like Gmail's search operators, but even Gmail allows for NOT terms.

The `zfind` tool has options to search every field. Once a field matches, you can use the show options to project values from the Zettel. There is also a `--count` option to tell you how many Zettels matched a query.

Find how many Zettels mention Chicago in the `summary` field:

```
zfind --database mlb.db --find-summary Chicago --count
1 Zettels matched search
```

...and print the `summary` and `filename` of the zettel:

```
zfind --database mlb.db --find-summary Chicago --count --show-filename
filename:
20170731132024-chicago-cubs.yaml

----------------------------------------

filename:
20170731155613-chicago-grey-sox.yaml

----------------------------------------

2 Zettels matched search
```

...and show the `summary` about the team:

```
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
```

Find the terms MLB and Central in the `note` field. Upon finding a  match, show the `filename` and the `summary` fields.

```
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
```

Find all zettels with Cubs mentioned in the `note` field:

```
zfind --database mlb.db --find-note Cubs --show-note

note:
The Chicago Cubs are an American professional baseball team based in Chicago, Illinois. The Cubs compete in Major League Baseball (MLB) as a member club of the National League (NL) Central division, where they are the defending World Series champions. The team plays its home games at Wrigley Field, located on the city's North Side. The Cubs are one of two major league teams in Chicago; the other, the Chicago White Sox, is a member of the American League (AL) Central division. The Cubs, first known as the White Stockings, was a founding member of the NL in 1876, becoming the Chicago Cubs in 1903.[2] The Cubs have appeared in a total of eleven World Series. The 1906 Cubs won 116 games, finishing 116–36 and posting a modern-era record winning percentage of .763, before losing the World Series to the Chicago White Sox by four games to two. The Cubs won back-to-back World Series championships in 1907 and 1908, becoming the first major league team to play in three consecutive World Series, and the first to win it twice. Most recently, the Cubs won the 2016 National League Championship Series and 2016 World Series, which ended a 71-year National League pennant drought and a 108-year World Series championship drought,
```

