# zimport.py - Import Zettels into an exising database

import os
import os.path
import sys
import yaml
import zdb

parser = zdb.get_argparse()
parser.add_argument('--zettel-dir', help="location of Zettels (path to folder)")
parser.add_argument('--validate', action="store_true", help="check Zettels only (don't import)", default=False)

args = parser.parse_args()
dir = args.zettel_dir
if not dir:
   parser.print_help()
   sys.exit(1)

db = zdb.get(args.database)

for filename in os.listdir(dir):
  if not filename.endswith('.yaml'):
    print("Ignoring %s; add .yaml extension to import this file." % filename)
    continue
  print("Importing %s" % filename)
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

    ydoc_id = 0
    for ydoc in ydocs:
      if type(ydoc) == type({}):
        ydoc['filename'] = filename
        if args.validate:
          errors = db.check(ydoc)
          if len(errors) > 0:
            if len(ydocs) > 0:
              print("-- The following messages are for Fass entry %d" % ydoc_id)
            for error in errors:
              print("-- " + error)
        else:
          db.bind(ydoc)
          db.insert_into_table()
      ydoc_id = ydoc_id + 1

db.done()

