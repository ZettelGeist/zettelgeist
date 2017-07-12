#
# zettel.py - a class that defines/restricts what is allowed in the Zettel.
# 
# All Zettel fields allow only a string or a list (of strings).
#

import argparse
import yaml
import zdb


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

class Zettel(object):

  FIELDS=['filename', 'title', 'tags', 'mentions', 'outline', 'cite', 'dates', 'summary', 'text', 'bibkey', 'bibtex', 'ris', 'inline', 'note', 'url' ]

  def __init__(self, filename=None):
    self.zettel = OrderedDict(zip(self.FIELDS, [None] * len(self.FIELDS)))

  def check_field(self, name):
    if name not in self.zettel:
       raise ZettelBadKey(name)

  def ensure_string(self, value):
    if not isinstance(value, str):
       raise ZettelStringRequired(value)

  def set_field(self, name, value, verbatim=False):
    self.check_field(name)
    self.ensure_string(value)
    if verbatim:
       self.zettel[name] = literal(value)
    else:
       self.zettel[name] = value

  def convert_to_list(self, name):
    self.check_field(name)
    value = self.zettel[name]
    if value == None:
       self.zettel[name] = []
    if isinstance(value, str):
       self.zettel[name] = [value]
    else:
       pass # we should never have a non-string or non-list entry but can put exception here if needed
   
  def append_field(self, name, value):
    self.convert_to_list(name)
    self.ensure_string(value)
    self.zettel[name].append(value)

  def load_field(self, name, filename):
    self.check_field(name)
    with open(filename, 'r') as infile:
      text = infile.read()
    self.set_field(name, text, True)

  def purge_unused_fields(self):
    unused_fields = [ name for name in self.zettel if self.zettel[name] == None ]
    for field in unused_fields:
      del(self.zettel[field])

  def get_yaml(self):
    self.purge_unused_fields()
    yaml.add_representer(quoted, quoted_presenter)
    yaml.add_representer(literal, literal_presenter)
    yaml.add_representer(OrderedDict, ordered_dict_presenter)
    return yaml.dump(self.zettel)


if __name__ == '__main__':
   parser = get_argparse()
   parser.print_help()
