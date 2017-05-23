#
# zcreate - create the Zettel database
#

import os.path
import argparse
import zdb

def parse_options():
  parser = argparse.ArgumentParser()
  parser.add_argument('--delete', action='store_const', const=True, default=False, help="delete the Zettel database file (not usually require)")
  return parser.parse_args()

def zcreate(args):
  if args.delete:
     zdb.delete()
  db = zdb.get()
  db.drop_table()
  db.create_table()
  db.done()


if __name__ == '__main__':
  args = parse_options()
  zcreate(args)
