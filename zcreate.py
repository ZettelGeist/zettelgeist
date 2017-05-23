#
# zcreate - create the Zettel database
#

import os.path
import argparse
import ftsdb

def parse_options():
  parser = argparse.ArgumentParser()
  parser.add_argument('--delete', action='store_const', const=True, default=False, help="delete the Zettel database file (not usually require)")
  return parser.parse_args()

def zcreate(args):
  if args.delete:
     fts.delete()
  zdb = ftsdb.get()
  zdb.drop_table()
  zdb.create_table()
  zdb.done()


if __name__ == '__main__':
  args = parse_options()
  zcreate(args)
