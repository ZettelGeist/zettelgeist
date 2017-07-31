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

When setting a field to a string value as we have done for each of these fields, it is permitted to have *embedded newlines* anywhere you like. For the note we have written, we havethree input lines, each of which appears on a separate line.

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





## Index and Find Zettels

