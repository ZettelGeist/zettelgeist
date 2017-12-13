# zcreate.py - create Zettel database

import os.path
import argparse
from . import zdb


def parse_options():
    parser = zdb.get_argparse()
    parser.add_argument('--delete', action='store_const', const=True,
                        default=False, help="delete if it already exists")
    return parser.parse_args()


def zcreate(args):
    if args.delete and os.path.exists(args.database):
        print("Deleting %s" % args.database)
        os.unlink(args.database)

    if not os.path.exists(args.database):
        print("Creating new database %s" % args.database)
        db = zdb.get(args.database)
        db.drop_table()
        db.create_table()
        db.done()
    else:
        print("Won't delete existing database %s" % args.database)
        print("- Rerun with --delete option to achieve this.")


def main():
    args = parse_options()
    zcreate(args)


if __name__ == '__main__':
    main()
