---
layout: page
title: Notes
permalink: /notes/
---

A note is nothing more than a YAML document. Please note that, hereafter, we may use the terms notes, cards, and zettels rather interchangeably. We've used other systems and sometimes find ourselves using the terminology rather freely.

When we use the term _note_, please keep in mind that the term as we see it is interchangeable with _index cards_, _cards_, or _Zettels_. So regardless of what terminlology you prefer, we welcome you!

Anyway, the idea of notetaking is to keep it simple, so a note should make no assumptions about formatting whatsoever. In our view of the world, we should be able to introduce other fields but are hopeful that we have identified most of the important ones.

In our current thinking, we have the following sections:

- title: an optional title (text)
- tags: one or more keywords (text, sequence of text, no nesting)
- mentions: one or more mentions (text, sequence of text, no nesting)
- outline: one or more items (text, sequence of text, nesting is permitted)
- dates (numeric text, sequence, must follow established historical ways of representing dates)
- text (text from the source as multiline string)
- bibtex, ris, or inline (text for the bibliographic item; will be syntax checked)
- bibkey (text, a hopefully unique identifier for referring to this source in other Zettels)
- cite: Used to cite a bibkey from the same or other notes. In addition, the citation may be represented as a list, where the first item is the bibkey and subsequent items are pages or ranges of page numbers. See below for a good example of how this will work.
- note: (any additional details that you wish to hide from indexing)

In most situations, freeform text is permitted. If you need to do crazy things, you must put quotes around the text so YAML can process it. However, words separated by whitespace and punctuation seems to work fine in most situations.

Some fields being contemplated for the future:

- todo: Indication of something to be researched in the course of preparing a particular note.

Semantic fields:

- wikipedia: the name of a Wikipedia page as it is often cited (even though many scholars pretend that they don't use it)
- youtube: ditto
- twitter: ditto

These all are intended to be string data, so there are no restrictions on what can be in any field; however, we will likely limit tags, mentions, dates in some way as we go forward. Fields such as bibtex, ris, or inline are also subject to validity checking.

```yaml
title: First BIB Note for Castells
tags:
  - Castells
  - Network Society
  - Charles Babbage is Awesome
  - Charles Didn't do Everything
mentions:
  - gkt
  - dbdennis
dates: 2016
cite:
  - Castells Rise 2016
  - ii-iv
  - 23-36
outline:
  - Introduction
  - - Computers
    - People
  - Conclusions
  - - Great Ideas of Computing

text: |
  Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam eleifend est sed diam maximus rutrum. Quisque sit amet imperdiet odio, id tristique libero. Aliquam viverra convallis mauris vel tristique. Cras ac dolor non risus porttitor molestie vel at nisi. Donec vitae finibus quam. Phasellus vehicula urna sed nibh condimentum, ultrices interdum velit eleifend. Nam suscipit dolor eu rutrum fringilla. Sed pulvinar purus purus, sit amet venenatis enim convallis a. Duis fringilla nisl sit amet erat lobortis dictum. Nunc fringilla arcu nec ex blandit, a gravida purus commodo. Vivamus lacinia tellus dui, vel maximus lacus ornare id.

  Vivamus euismod justo sit amet luctus bibendum. Integer non mi ullamcorper enim fringilla vulputate sit amet in urna. Nullam eu sodales ipsum. Curabitur id convallis ex. Duis a condimentum lorem. Nulla et urna massa. Duis in nibh eu elit lobortis vehicula. Mauris congue mauris mollis metus lacinia, ut suscipit mi egestas. Donec luctus ante ante, eget viverra est mollis vitae.

  Vivamus in purus in erat dictum scelerisque. Aliquam dictum quis ligula ac euismod. Mauris elementum metus vel scelerisque feugiat. Vivamus bibendum massa eu pellentesque sodales. Nulla nec lacus dolor. Donec scelerisque, nibh sed placerat gravida, nunc turpis tristique nibh, ac feugiat enim massa ut eros. Nulla finibus, augue egestas hendrerit accumsan, tellus augue tempor eros, in sagittis dolor turpis nec mi. Nunc fringilla mi non malesuada aliquet.

bibkey:
  Castells Rise 1996
bibtex: |
  @book{castells_rise_1996,
    address = {Cambridge, Mass.},
    series = {Castells, {Manuel}, 1942- {Information} age . v},
    title = {The rise of the network society},
    isbn = {978-1-55786-616-5},
    language = {eng},
    publisher = {Blackwell Publishers},
    author = {Castells, Manuel},
    year = {1996},
    keywords = {Information networks., Information society., Information technology Economic aspects., Information technology Social aspects., Technology and civilization.}
  }

note:
  A sample Zettel.
```
