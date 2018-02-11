import sys
import argparse
from zettelgeist import zdb, zettel, zquery


def get_argparse():
    parser = zdb.get_argparse()
    parser.add_argument('--use-zettel', action='store_const',
                        const=True, default=False)

    for field in zdb.ZettelSQLFields:
        parser.add_argument('--show-%s' % field,
                            action='store_const', const=True, default=False,
                            help="include field <%s> in output" % field)

    parser.add_argument('--count', action='store_const', const=True,
                        default=False, help="Show number of Zettels matching this search")
    parser.add_argument('--query-prompt', action='store_const', const=True,
                        default=False, help="enter query interactively (overrides --input))")

    parser.add_argument(
        '--query-file', help="load query from file", default=None)

    parser.add_argument(
        '--query', help="query from command line (use single quotes)", default=None)
    return parser


def main():
    parser = get_argparse()
    args = parser.parse_args()
    argsd = vars(args)

    if args.query_prompt:
        input_line = input("zfind:zql> ")
    elif args.query_file:
        with open(args.query_file) as infile:
            input_line = infile.read()
    elif args.query:
        input_line = args.query
    else:
        input_line = None

    if input_line:
        ast = zquery.compile(input_line)
        db = zdb.get(args.database)
        gen = db.fts_query(ast[0])
    else:
        print("Warning: Query could not be loaded via --query, --query-file, or --query-prompt")
        sys.exit(1)

    search_count = 0
    for row in gen:
        search_count = search_count + 1
        printed_something = False
        if args.use_zettel:
            loader = zettel.ZettelLoader(row['filename'])
            zettels = loader.getZettels()
            z = next(zettels)
        else:
            z = None

        for field in row.keys():
            show_field = "show_" + field
            if argsd.get(show_field, None):
                if row[field]:
                    if z and field in zettel.ZettelFields:
                        print(z.get_yaml([field]))
                    else:
                        print("%s:" % field)
                        print(row[field])
                        print()
                    printed_something = True

        if printed_something:
            print("-" * 3)
            print()

    if args.count:
        print("%d Zettels matched search" % search_count)


if __name__ == '__main__':
    main()
