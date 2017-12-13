# zimport.py - Import Zettels into an exising database

import os
import os.path
import sys
import yaml
from . import zdb, zettel


def get_zettels(dir):
    for (dirpath, dirnames, filenames) in os.walk(dir):
        for filename in filenames:
            if filename.endswith('.yaml'):
                yield os.path.join(dirpath, filename)


def main():
    parser = zdb.get_argparse()
    parser.add_argument(
        '--dir', help="location of Zettels (path to folder)", required=True)
    parser.add_argument('--validate', action="store_true",
                        help="check Zettels only (don't import)", default=False)

    args = parser.parse_args()
    db = zdb.get(args.database)
    zettel_dir = args.dir

    for filepath in get_zettels(zettel_dir):
        if not filepath.endswith('.yaml'):
            print("Ignoring %s; add .yaml extension to import this file." % filepath)
            continue
        print("Importing %s" % filepath)
        with open(filepath) as infile:
            try:
                text = infile.read()
            except:
                print("- I/O error on %s: Encoding must be UTF-8" % filepath)
                continue
            try:
                ydocs = yaml.load_all(text)
            except:
                print("- YAML load failure (run yamllint on this file)")
                continue

            try:
                ydoc = next(ydocs)
            except:
                print("- YAML loaded but could not be processed")
                continue

            if isinstance(ydoc, dict):
                try:
                    z = zettel.Zettel(ydoc)
                except zettel.ParseError as error:
                    error_text = str(error)
                    print("%s:\n%s" % (filepath, error_text))
                    continue

                if not args.validate:
                    db.bind(z, filepath)
                    db.insert_into_table()

    db.done()


if __name__ == '__main__':
    main()
