# zimport.py - Import Zettels into an exising database

import os
import os.path
import sys
import frontmatter # to accommodate Markdown with YAML frontmatter

from . import zdb, zettel

import yaml
try:
   from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
   from yaml import Loader, Dumper


def get_zettels(dir):
    for (dirpath, dirnames, filenames) in os.walk(dir):
        for filename in filenames:
            if filename.endswith('.yaml') or filename.endswith('.md'):
                yield os.path.join(dirpath, filename)


def main():
    parser = zdb.get_argparse()
    parser.add_argument(
        '--dir', help="location of Zettels (path to folder)", required=True)

    parser.add_argument('--fullpath', action="store_true",
                        help="store full path to file in index", default=False)

    parser.add_argument('--validate', action="store_true",
                        help="check Zettels only (don't import)", default=False)

    parser.add_argument('--create', action="store_true",
                        help="create database and delete existing if present", default=False)

    args = parser.parse_args()

    if args.create or not os.path.exists(args.database): 
        zcreate(args)

    db = zdb.get(args.database)
    zettel_dir = args.dir

    for entry in get_zettels(zettel_dir):
        if args.fullpath:
            filepath = os.path.abspath(entry)
        else:
            filepath = entry
        print("Processing %s" % filepath)
        if filepath.endswith('.yaml'):
            yaml_info = zettel.load_pure_yaml(filepath)
        elif filepath.endswith('.md'):
            yaml_info = zettel.load_markdown_with_frontmatter(filepath)
        else:
            print("Warning: %s is not .yaml or .md (ignoring)")

        (ydoc, document) = yaml_info
        if len(ydoc) > 0:
            try:
                z = zettel.Zettel(ydoc)
            except zettel.ParseError as error:
                error_text = str(error)
                print("%s:\n%s" % (filepath, error_text))
                continue

            if not args.validate:
                db.bind(z, filepath, document)
                db.insert_into_table()

    db.done()


def zcreate(args):
    if os.path.exists(args.database):
        print("Deleting existing database %s" % args.database)
        os.unlink(args.database)
    print("Creating new database %s" % args.database)
    db = zdb.get(args.database)
    db.drop_table()
    db.create_table()
    db.done()

if __name__ == '__main__':
    main()
