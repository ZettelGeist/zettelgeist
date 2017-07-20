#
# zettel.py - A checker for Zettels
#

import argparse
import yaml
from zettelgeist import zdb

# Recursive descent parsing of Zettel dictionary format.

class ParseError(Exception):
  def __init__(self, message):
    self.message = message

  def __str__(self):
    return self.message

def typename(value):
  return type(value).__name__

def parse_zettel(doc):
  if not isinstance(doc, dict):
    raise ParseError("Zettels require key/value mappings at top-level. Found %s" % typename(doc))

  # These fields are all optional but, if present, must be strings
  parse_string_field(doc, 'title')
  parse_string_field(doc, 'bibkey')
  parse_string_field(doc, 'bibtex')
  parse_string_field(doc, 'ris')
  parse_string_field(doc, 'inline')
  parse_string_field(doc, 'url')
  parse_string_field(doc, 'summary')
  parse_string_field(doc, 'comment')
  parse_string_field(doc, 'note')
  
  # These fields are all optional but, if present, must be list of strings  
  
  parse_list_of_string_field(doc, 'tags')
  parse_list_of_string_field(doc, 'mentions')

  parse_citation(doc, 'cite')
  parse_dates(doc, 'dates')

  # TODO: Check for extraneous fields in all cases

def parse_string_field(doc, field, required=False):
  value = doc.get(field, None)
  if value == None:
    if required: 
      raise ParseError("Field %s requires a string but found %s of type %s" % (field, value, typename(value)))
    return
  if not isinstance(value, str):
    raise ParseError("Field %s must be a string or not present at all - found value %s of type %s" % (field, value, typename(value)))


def parse_list_of_string_field(doc, field, required=False):
  value = doc.get(field, None)
  if value == None:
    if required: 
      raise ParseError("Field %s requires a list of strings" % field)
    return
  if not isinstance(value, (list, tuple)):
    raise ParseError("Field %s must be a list or not present at all - foudn value %s of type %s" % (field, value, typename(value)))

  # Make a dictionary of the list items for checking purposes only
  # That is, treat the list like a dictionary. Will simplify with comprehension magic later
  doc2 = {}
  pos = 0
  for item in value:
    doc2["%s(%d)" % (field, pos)] = item    
  for key in doc2.keys():
    parse_string_field(doc2, key, True)

def parse_citation(doc, field):
  value = doc.get(field, None)
  if value == None:
    return
  if not isinstance(value, dict):
    raise ParseError("%s must be a nested (citation) dictoinary" % field)
  parse_string_field(value, 'bibkey', True)
  parse_string_field(value, 'page')

def parse_dates(doc, field):
  value = doc.get(field, None)
  if value == None:
    return
  if not isinstance(value, dict):
    raise ParseError("%s must be a nested (dates) dictionary" % field)
  parse_string_field(value, 'year', True)
  parse_string_field(value, 'era')

# This is to support formatting of resulting YAML (after modification of the underlying dictionary)
   
from collections import OrderedDict

class quoted(str):
  pass

def quoted_presenter(dumper, data):
  return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')

class literal(str):
  pass

def literal_presenter(dumper, data):
  return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')

def ordered_dict_presenter(dumper, data):
  return dumper.represent_dict(data.items())

class ZettelBadKey(Exception):
  def __init__(self, name):
    self.name = name

class ZettelStringRequired(Exception):
  def __init__(self, value):
    self.value = value

def get_argparse():
  parser = argparse.ArgumentParser()
  parser.add_argument('--database', help="alternate database name", default=zdb.ZDB)
  for field in Zettel.FIELDS:
     parser.add_argument('--set-%s' % field, help="set the value of field %s" % field)
     parser.add_argument('--append-%s' % field, help="add value to field %s" % field)
     parser.add_argument('--erase-%s' % field, help="remove field %s" % field)
     parser.add_argument('--load-%s' % field, help="load field from %s" % field)
  return parser

def flatten(item):
    if item == None:
        return [""]
    elif isinstance(item, dict):
        return flatten([ ":".join([k, item[k]]) for k in item ])
    elif not isinstance(item, (tuple, list)):
        return [str(item)]

    if len(item) == 0:
        return item
    else:
        return flatten(item[0]) + flatten(item[1:])

class Zettel(object):

  def __init__(self, data):
    self.zettel = data
    parse_zettel(self.zettel)

  def set_field(self, name, value):
    self.zettel[name] = value
    parse_zettel(self.zettel)

  def delete_field(self, name):
    del(self.zettel[name])
    parse_zettel(self.zettel)

  def reset_list_field(self, name):
    self.zettel[name] = []
    parse_zettel(self.zettel)

  def append_list_field(self, name, value):
    self.zettel[name].append(value)
    parse_zettel(self.zettel)

  def set_citation(self, bibkey, page=None):
    citation = { 'bibkey' : bibkey }
    if page != None:
      citation['page'] = page
    self.zettel['cite'] = citation
    parse_zettel(self.zettel)

  def set_dates(self, year, era=None):
    dates = { 'year' : year }
    if era != None:
      dates['era'] = era
    self.zettel['dates'] = dates
    parse_zettel(self.zettel)

  def load_field(self, name, filename):
    with open(filename, 'r') as infile:
      text = infile.read()
    self.set_field(name, text)
    parse_zettel(self.zettel)

  def get_yaml(self):
    #yaml.add_representer(quoted, quoted_presenter)
    #yaml.add_representer(literal, literal_presenter)
    #yaml.add_representer(OrderedDict, ordered_dict_presenter)
    return yaml.dump(self.zettel)

  def get_indexed_representation(self):
    parse_zettel(self.zettel)
    return { key : ",".join(flatten(self.zettel[key])) for key in self.zettel}


#
# This generic loader can be used in any module that needs to work on a Fass or Stein
# Will be used mainly by zimport.py
#

class ZettelLoaderError(Exception):
  def __init__(self, message):
    self.message = message

class ZettelLoader(object):
  def __init__(self, filename):
    with open(filename) as infile:
      try:
        text = infile.read()
      except:
        raise ZettelLoaderError("%s: I/O error - Encoding must be UTF-8" % filename)
    try:
      self.ydocs = yaml.load_all(text)
    except:
      raise ZettelLoaderError("%s: YAML load failure" % filename)

  def getZettels(self):
    ydoc_id = 0
    for ydoc in self.ydocs:
      if isinstance(ydoc, dict):
        try:
          oneZettel = zettel.Zettel(ydoc)
          yield (ydoc_id, oneZettel, None)
        except zettel.ParseError as error:
          yield (ydoc_id, None, error)
      ydoc_id = ydoc_id + 1

if __name__ == '__main__':
   parser = get_argparse()
   parser.print_help()
