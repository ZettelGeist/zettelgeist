from ftsdb import getDB
import sys
import os
import os.path
import yaml

dir = sys.argv[1]
zdb = getDB()

print("dir = %s" % dir)
for filename in os.listdir(dir):
  print("Processing %s" % filename)
  filepath = os.path.join(dir, filename)
  with open(filepath) as infile:
    try:
       text = infile.read()
    except:
       print("Could not read() from file %s" % filename)
       text = ""
    try:
       ydocs = yaml.load_all(text)
    except:
       continue

    try:
      ydocs = list(ydocs)
    except:
      print("errors in filename %s" % filename)
      continue

    for ydoc in ydocs:
      if type(ydoc) == type({}):
         ydoc['filename'] = filename
         zdb.bind(ydoc)
         zdb.insert_into_table()

zdb.done()

