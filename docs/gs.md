---
layout: page
title: User's Guide
permalink: /gs/
---

# Summary

ZettelGeist performs two basic operations: writing note cards and retrieving them.
The tool for writing cards is `zettel`.
Since cards are stored as [`yaml`](https://en.wikipedia.org/wiki/YAML), `zettel` is essentially a command-line tool for writing new `yaml` documents and editing existing ones.
The functionality of this tool will be illustrated first.
We will turn then to `zcreate`, `zimport`, and `zfind`, the tools for collecting cards into a database and running queries on it.

# Prerequisites

This user's guide assumes that you have installed ZettelGeist and confirmed its tools are available in a Python virtual environment.
See the [Installation](/install) page for instructions. 
You must source the virtual environment to use ZettelGeist.
We will assume that your virtual environment is named `zenv`.

# Writing cards with `zettel`

## Synopsis

`zettel` [--file *input-file*] \[*options*] ...

If no input file is specified, input is read from the options passed to `zettel` in standard input.
Output goes by default to standard output.
For output to a file, use the option `--save` (to write the filename yourself) or `--name` (to have `zettel` write the filename for you).

## Getting help

```shell
(zenv) $ zettel --help
```

Most options have a regular verb-object syntax and instruct `zettel` to do a specified action (`set`, `append`, `prompt`, `load` or `delete`) on a field-value.
Examples will be given below.

## Create and save a simple zettel

```shell
(zenv) $ zettel --set-title "Hello, World!"
```

This results in the following output:

```yaml
title: Hello, World!
```

To write this output to a file, invoke the `--save` option:

```shell
(zenv) $ zettel --set-title "Hello, World!" --save template.yaml
```

A basic ZettelGeist workflow consists in writing a template-card to be invoked and edited in subsequent iterations.
Here is an example: 

```shell
(zenv) $ zettel --file template.yaml --set-note "A Zettel with a note" --name timestamp
```

This command reads two input sources, merges them, and saves output to a new file with the following content:

```yaml
title: Hello, World!
note: A Zettel with a note
```

Writing long strings in command line arguments is inconvenient, so ZettelGeist provides two alternatives.
The option `--prompt-<FIELD>` divides card-writing into steps.
When this option is invoked, `zettel` will request input for the specified field before creating a new card.
Text is entered within the terminal.
Newlines and blank lines are permitted.
Type `ctrl+d` to complete input.

```shell
(zenv) $ zettel --file template.yaml --prompt-note --name timestamp
```

The option `--load-<FIELD>` reads input for the specified field from a text file:

```shell
(zenv) $ zettel --file template.yaml --load-note some.txt --name timestamp
```

The `timestamp` value ensures that no two cards will have the same file name, but it masks file content.
The `--id` option feeds a descriptive string into the file name:

```shell
(zenv) $ zettel --file template.yaml --id tutorial --name id timestamp
```

To serialize cards rather assigning a timestamp to them, use the `--counter` option:

```shell
(zenv) $ zettel --file template.yaml --id tutorial --counter tutorial --name id counter
```

This command initiates a count of cards with the `id` "tutorial".
The count is maintained in a new binary file `.counter.dat`.
The default number of digits is four and the count starts at `0000`.
The values `id`, `counter`, and `timestamp` may be combined in any order.

## ZettelGeist fields

The preceding section introduced the fields `title` and `note`.
In this section we provide a full list of ZettelGeist fields and the operations that may be performed on them.

For fields with a string value, the option `--set-<FIELD>` inputs a value for that field, as we saw in the previous section.
For fields with a list value, use the `--append-<FIELD>` and place each value within quotes.
Examples will be provided below for the relevant fields. 

All fields are user-defined.
We provide suggestions based on our own workflows.

### `bibkey`

(String.) 
A unique identifier for the source from which you have extracted this note.
Users of the [Better BibTex](https://retorque.re/zotero-better-bibtex/) extension for [Zotero](https://www.zotero.org/) may want to enter the Better BibTex Citation Key in this field.

### `bibtex`

A BibTex citation.
This field is redundant if you manage your bibliography with Zotero and tie note-cards to Zotero items with Better BibTex Citation Keys in the field `bibkey`.
<!-- ris, or inline (string) -->

### `cite`

This field has two child fields, `bibkey` (redundant with the field above) and `page`.
Values must be supplied for both child fields and placed in quotes.
For instance:

```shell
--set-cite "FoucaultArchaeologyKnowledgeDiscourse1982" "pp. 103-4"
```

When creating a template card, enter a dummy value for `page`:

```shell
--set-cite "FoucaultArchaeologyKnowledgeDiscourse1982" "p."
```

When calling a template card with the `--file` option, the following syntax will update `cite` values:

```shell
--set-cite "" "pp. 103-4"
```

This command retains the `bibkey` value in the input file but replaces the previous `page` value with "pp. 103-4".

### `comment`

(String.)
Any comment you want to make about the zettel in general.

### `dates`

A `year` (string) and `era` (string) as a nested dictionary.
Syntax follows `cite`.

### `mentions`

(List.)
One or more mentions.
Use the option `--append-mentions` and put each within quotes. 
For instance: `--append-mentions "Sievers, Eduard" "Lachmann, Karl"`.

### `note`

(String.)
This is the core element of the note card.
Usually it is a quotation extracted from the source and page identified in the `cite` field.

### `summary`

(String.)
A concise summary of the note (by convention).

### `tags`

(List.) 
One or more keywords.
Use the option `--append-tags` and put each keyword within quotes. 
For instance: `--append-tags "Charles Babbage" "Ada Lovelace" "Victorian Era"`.

### `title`
(String.)
A human-readable label for a sequence of note cards. 
We set this label in the template card for a source and retain it in all note cards on that source.

### `url`

(String.)
Useful for bookmarking websites.

# Retrieving cards

We now describe tools for selectively retrieving cards.
`zcreate` creates a new empty database.
`zimport` populates the database with note cards.
`zfind` runs queries on the database and returns matching cards.

## Synopsis

```zcreate --database <NAME>.db```

```zimport --database <NAME>.db --dir $(pwd)```

```zfind --database <NAME>.db  --query-string 'FIELD:"VALUE"' ``` [*options*]

## A tutorial

To illustrate the function of these tools, we use sample zettels published 
at https://github.com/ZettelGeist/zg-tutorial.git. 
Download the repository with `git clone`:

```shell
$ git clone https://github.com/ZettelGeist/zg-tutorial.git
```

This creates a new directory `zg-tutorial`.
Enter `zg-tutorial/zettels/baseball` and list its contents: 

```shell
$ cd zg-tutorial/zettels/baseball
$ ls
```

<!-- the arguments passed to zimport capture all zetteln in working dir and subdirectories. To import baseball zetteln only, this operation must be performed from the baseball dir -->

Use `cat` to take a look at one of the cards.

```yaml
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
```

### Create a database

We will now import the cards into a database.
First, create a new database: 

```shell
(zenv) $ zcreate --database mlb.db
Creating new database mlb.db
```

Next, populate the database: 

```shell
(zenv) $ zimport --database mlb.db --dir $(pwd)
```

We are now ready to run queries on the database and selectively retrieve cards from it.

### Run queries

Searching is done with the `zfind` tool.
The option `--query-string` tells `zfind` what to look for.
The options `--count` and `--show-<FIELD>` tell `zfind` what to do with matches:

- `--count` counts the cards matching the search criteria and prints that number to standard output.
- `--show-<FIELD>` prints the specified field to standard output.

These output options may be combined. `--show-<FIELD>` may be repeated with different fields.

The basic syntax of `--query-string` is `'KEY:"VALUE"'`.
This syntax is illustrated in the following examples: 

1. To find how many cards mention Chicago in the `summary` field

```shell
(zenv) $ zfind --database mlb.db --query-string 'summary:"Chicago"' --count
2 Zettels matched search
```

2. To print the matching summaries and filenames

```shell
(zenv) $ zfind --database mlb.db --query-string 'summary:"Chicago"' --show-filename --show-summary
summary: Chicago White Sox

filename:
/path/to/chicago-grey-sox.yaml

---

summary: Chicago Cubs

filename:
/path/to/chicago-cubs.yaml

---
```

3. To find the phrase "Central division" in the `note` field and print the `summary` fields

```shell
(zenv) $ zfind --database mlb.db --query-string 'note:"Central division"' --show-summary
summary: Minnesota Twins

---

summary: Pittsburgh Pirates

---

summary: Cincinnati Reds

---

summary: Detroit Tigers

---

summary: Cleveland Indians

---

summary: St. Louis Cardinals

---

summary: Chicago Cubs

---

summary: Kansas City Royals

---
```

4. To find all cards with Cubs mentioned in the `note` field and print that field

```shell
(zenv) $ zfind --database mlb.db --query-string 'note:"Cubs"' --show-note

note: |
  The Chicago Cubs are an American professional baseball team based in Chicago, Illinois. The Cubs
  compete in Major League Baseball (MLB) as a member club of the National League (NL) Central
  division, where they are the defending World Series champions. The team plays its home games at
  Wrigley Field, located on the city's North Side. The Cubs are one of two major league teams in
  Chicago; the other, the Chicago White Sox, is a member of the American League (AL) Central
  division. The Cubs, first known as the White Stockings, was a founding member of the NL in 1876,
  becoming the Chicago Cubs in 1903.[2] The Cubs have appeared in a total of eleven World Series.
  The 1906 Cubs won 116 games, finishing 116–36 and posting a modern-era record winning percentage
  of .763, before losing the World Series to the Chicago White Sox by four games to two. The Cubs
  won back-to-back World Series championships in 1907 and 1908, becoming the first major league
  team to play in three consecutive World Series, and the first to win it twice. Most recently,
  the Cubs won the 2016 National League Championship Series and 2016 World Series, which ended a
  71-year National League pennant drought and a 108-year World Series championship drought,

---
```

To save this output, redirect standard output to a file with `>`: 

```shell
(zenv) $ zfind --database mlb.db --query-string 'note:"Cubs"' --show-note > new-file.txt
```