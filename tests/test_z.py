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
  zettel.parse_zettel(zdict)



