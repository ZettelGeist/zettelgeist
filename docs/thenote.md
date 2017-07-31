---
layout: page
title: Note Format
permalink: /notes/
---

A note is nothing more than a YAML document. Please note that, hereafter, we may use the terms notes, cards, and zettels rather interchangeably. We've used other systems and sometimes find ourselves using the terminology rather freely.

When we use the term _note_, please keep in mind that the term as we see it is interchangeable with _index cards_, _cards_, or _zettels_. So regardless of what terminlology you prefer, we welcome you!

Anyway, the idea of notetaking is to keep it simple, so a note should make no assumptions about formatting whatsoever. In our view of the world, we should be able to introduce other fields but are hopeful that we have identified most of the important ones.

In our current thinking, we have the following sections:

- title: an optional title (string)
- tags: one or more keywords (list of string)
- mentions: one or more mentions (list of string)
- dates: a year (string) and era (string) as a nested dictionary
- bibtex, ris, or inline (string)
- url (string)
- bibkey (string)
- cite: a bibkey (from same or another zettel) and a page number (or range of page numbers)
- summary: (string) - concise summary of the note (by convention)
- note (string) - details, usually the text you are wanting to cite
- comment (string) - any comment you want to make about the zettel in general

In most situations, freeform text is permitted. In some situations, you will need to put quotes around
the text, especially if you are using reserved YAML characters.

These all are intended to be string data, so there are no restrictions on what can be in any field; however, we will likely limit tags, mentions, dates in some way as we go forward. Fields such as bibtex, ris, or inline are also subject to validity checking.

Here's an example where of a zettel where most fields are being used.

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
dates:
  year: "2016"
  era: "AD"
cite:
  bibkey: Castells Rise 2016
  page: ii-iv
comment: This is my first zettel but my comments have nothing to do with the note itself.
summary: Lorem ipsum rocks. This is a summary of what you see in the note field.
note: |
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

```

Here is a simple example of a bookmark:

```yaml
title: Zettelgeist.com
url: http://zettelgeist.com
note: Zettelgeist is a plaintext notetaking system designed for scholarly/research purposes.
```

