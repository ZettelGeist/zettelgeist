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
        'title': "Valid title"
    }
    zettel.parse_zettel(doc)


def test_parse_simple_bad_value():
    doc = {
        'title': 35
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


def test_creator_and_load():
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
    text = z.get_yaml()

    ydoc = yaml.load(text)
    z2 = zettel.Zettel(ydoc)
    text2 = z2.get_yaml()
    assert text == text2


def test_creator_and_load_optional_fields():
    z = zettel.Zettel({})
    z.set_field('title', 'My First Zettel')
    z.reset_list_field('mentions')
    z.append_list_field('mentions', 'dbdennis')
    z.append_list_field('mentions', 'gkt')
    z.reset_list_field('tags')
    z.append_list_field('tags', 'Charles Babbage')
    z.append_list_field('tags', 'Ada Lovelace')
    z.set_citation('Ifrah')
    z.set_dates('1841')
    z.set_field('summary', 'An amazing Zettel')
    z.set_field('note', 'Text of Zettel')
    z.set_field('bibkey', 'BibKey')
    z.set_field('bibtex', '@article{ley, entries}')
    text = z.get_yaml()

    ydoc = yaml.load(text)
    z2 = zettel.Zettel(ydoc)
    text2 = z2.get_yaml()
    assert text == text2


def test_zettel_fts_strings():
    z = zettel.Zettel({})
    z.set_field("title", "title")
    z.set_field("summary", "a summary")
    expected = {'title': 'title', 'summary': 'a summary'}
    z.get_indexed_representation() == expected


def test_zettel_fts_lists():
    z = zettel.Zettel({})
    z.reset_list_field("tags")
    z.append_list_field("tags", "Babbage")
    z.append_list_field("tags", "Lovelace")
    expected = {'tags': 'Babbage,Lovelace'}
    z.get_indexed_representation() == expected


def test_zettel_fts_cite():
    z = zettel.Zettel({})
    z.set_citation("Castells 2006", "ii-iv")
    z.get_indexed_representation()
    expected = {'cite': 'bibkey:Castells 2006,page:ii-iv'}
    z.get_indexed_representation() == expected

    z.set_citation("Castells 2006")  # omitting page numbers
    expected = {'cite': 'bibkey:Castells 2006'}
    z.get_indexed_representation() == expected


def test_zettel_fts_dates():
    z = zettel.Zettel({})
    z.set_dates('2006', 'CE')
    expected = {'dates': 'year:2006,era:CE'}
    z.get_indexed_representation() == expected

    z.set_dates('2006')  # omit era
    expected = {'dates': 'year:2006'}
    z.get_indexed_representation() == expected


def test_invalid_zettel_fields():
    z = zettel.Zettel({})
    with pytest.raises(zettel.ParseError):
        z.set_field('blah', 'blah')
    z.delete_field('blah')

    # checks for injection of bad values in nested citation dictionary
    z.set_citation('Castells 2006', 'ii-iv')
    with pytest.raises(zettel.ParseError):
        z.zettel['cite']['blah'] = 'blah'
        z.get_yaml()  # force checks

    del(z.zettel['cite']['blah'])

    # checks for injection of bad values in nested dates dictionary
    z.set_dates('2006', 'CE')
    with pytest.raises(zettel.ParseError):
        z.zettel['dates']['blah'] = 'blah'
        z.get_yaml()
    del(z.zettel['dates']['blah'])
