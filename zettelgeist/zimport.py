# zimport.py - Import Zettels into an exising database

import os
import os.path
import sys
import yaml
from zettelgeist import zdb, zettel

def main():
    parser = zdb.get_argparse()
    parser.add_argument(
        '--zettel-dir', help="location of Zettels (path to folder)")
    parser.add_argument('--validate', action="store_true",
                        help="check Zettels only (don't import)", default=False)

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

            fass_id = zettel.gen_id()
            for ydoc in ydocs:
                if isinstance(ydoc, dict):
                    try:
                        z = zettel.Zettel(ydoc)
                    except zettel.ParseError as error:
                        error_text = str(error)
                        print("%s:\n%s" % (filepath, error_text))
                        continue
                    finally:
                        this_fass_id = next(fass_id)

                    if not args.validate:
                        print("%s: fass entry %d" % (filename, this_fass_id))
                        db.bind(z, filename, this_fass_id)
                        db.insert_into_table()

    db.done()


if __name__ == '__main__':
    main()
