from ftsdb import getDB
import sys
import yaml

files = sys.argv[1:]

zdb = getDB()

for filename in files:
  with open(filename) as infile:
    text = infile.read()
    ydocs = yaml.load_all(text)
    for ydoc in ydocs:
      if type(ydoc) == type({}):
         ydoc['filename'] = filename
         print(ydoc.keys())
         #zdb.bind(ydoc)
         #zdb.insert_table()

zdb.done()

