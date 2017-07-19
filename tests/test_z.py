import sys
import textwrap
import yaml

from zettelgeist import zettel

# content of test_sysexit.py
import pytest

def f():
  raise SystemExit(1)

def test_mytest():
  with pytest.raises(SystemExit):
    f()

def test_parse_empty():
  doc = {}
  zettel.parse_zettel(doc)

def test_parse_simple_valid():
  doc = {
    'title' : "Valid title"
  }
  zettel.parse_zettel(doc)

def test_parse_simple_bad_value():
  doc = {
    'title' : 35
  }
  with pytest.raises(zettel.ParseError):
    zettel.parse_zettel(doc)

def test_simple_zettel():
  zdoc = """
    title: My First Zettel
    mentions:
    - dbdennis
    - gkt
    tags:
    - Charles Babbage
    - Ada Lovelace
    cite:
      bibkey: Ifrah
      page: "22-36"
    dates:
      year: "1841"
      era: CE
    summary: An amazing Zettel
    note: Text of Zettel
    bibkey: BibKey
    bibtex: "@article{key, entries}"
    """
  zdoc = textwrap.dedent(zdoc)
  print(zdoc)
  zdict = yaml.load(zdoc)
  z = zettel.Zettel(zdict)

def test_creator():
  z = zettel.Zettel({})
  z.set_field('title', 'My First Zettel')
  z.reset_list_field('mentions')
  z.append_list_field('mentions', 'dbdennis')
  z.append_list_field('mentions', 'gkt')
  z.reset_list_field('tags')
  z.append_list_field('tags', 'Charles Babbage')
  z.append_list_field('tags', 'Ada Lovelace')
  z.set_citation('Ifrah', '22-36')
  z.set_dates('1841', 'CE')
  z.set_field('summary', 'An amazing Zettel')
  z.set_field('note', 'Text of Zettel')
  z.set_field('bibkey', 'BibKey')
  z.set_field('bibtex', '@article{ley, entries}')
  z.get_yaml()




