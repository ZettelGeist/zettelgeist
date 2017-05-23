
import ftsdb

import argparse
parser = argparse.ArgumentParser()

for field in ftsdb.ZETTEL_FIELDS:
   parser.add_argument('--find-%s' % field, help='search the YAML %s field' % field)
   parser.add_argument('--exclude-%s' % field, help='search the YAML %s field' % field)
   parser.add_argument('--show-%s' % field, action='store_const', const=True, default=False)

args = parser.parse_args()

argsd = vars(args)
query = []
for field in ftsdb.ZETTEL_FIELDS:
   exclude_field = 'exclude_' + field
   include_field = 'find_' + field
   if exclude_field in argsd:
      entry = argsd.get(exclude_field)
      if entry: query.append((field, '-', entry))
   if include_field in argsd:
      entry = argsd.get(include_field)
      if entry: query.append((field, '', entry))

db = ftsdb.get()
gen = db.fts_search(query)

for row in gen:
   printed_something = False
   for field in row.keys():
      show_field = "show_" + field
      if argsd.get(show_field, None):
         if len(row[field]) > 0:
            print("%s:" % field)
            print(row[field])
            print()
            printed_something = True
         
   if printed_something:
      print("-" * 40)
      print()
