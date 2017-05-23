
import ftsdb

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--find-text', help='search the YAML text field')
parser.add_argument('--exclude-text', help='search the YAML text field')
parser.add_argument('--find-title', help='search the YAML title field')
parser.add_argument('--exclude-title', help='search the YAML title field')
parser.add_argument('--show-filename',  action='store_const', const=True, default=False)
parser.add_argument('--show-title',  action='store_const', const=True, default=False)
parser.add_argument('--show-text',  action='store_const', const=True, default=False)
args = parser.parse_args()

print(args)

argsd = vars(args)
query = []
for field in ['text', 'title']:
   exclude_field = 'exclude_' + field
   include_field = 'find_' + field
   if exclude_field in argsd:
      entry = argsd.get(exclude_field)
      if entry: query.append(('-', field, entry))
   if include_field in argsd:
      entry = argsd.get(include_field)
      if entry: query.append(('', field, entry))

db = ftsdb.get()
gen = db.fts_search(query)

for row in gen:
   for field in row.keys():
      show_field = "show_" + field
      if argsd.get(show_field, None):
         if len(row[field]) > 0:
            print("%s = %s" % (field, row[field]))
   print()
