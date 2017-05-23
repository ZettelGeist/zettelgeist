import zdb
import sys
import os
import os.path
import yaml

dir = sys.argv[1]
db = zdb.get()

print("dir = %s" % dir)
for filename in os.listdir(dir):
  if not filename.endswith('.yaml'):
    continue
  print("%s:" % filename)
  filepath = os.path.join(dir, filename)
  with open(filepath) as infile:
    try:
       text = infile.read()
    except:
       print("- I/O error on %s: Encoding must be UTF-8" % filename)
       continue
    try:
       ydocs = yaml.load_all(text)
    except:
       print("- YAML load failure (run yamllint on this file)")
       continue

    try:
      ydocs = list(ydocs)
    except:
      print("- YAML loaded but could not be processed")
      continue

    for ydoc in ydocs:
      if type(ydoc) == type({}):
         ydoc['filename'] = filename
         db.bind(ydoc)
         db.insert_into_table()

db.done()

