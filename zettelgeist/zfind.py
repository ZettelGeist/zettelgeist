import sys
import argparse
import yaml
from . import zdb, zettel, zquery


def get_argparse():
    parser = zdb.get_argparse()
    parser.add_argument('--use-index', action='store_const',
                        const=True, default=False)
    parser.add_argument('--verbatim', action='store_const',
            const=True, default=False)

    for field in zdb.ZettelSQLFields:
        # parser.add_argument('--find-%s' %
        #                    field, help='search the Zettel %s field' % field)
        # parser.add_argument('--exclude-%s' %
        #                    field, help='search the Zettel %s field' % field)
        parser.add_argument('--show-%s' % field,
                            action='store_const', const=True, default=False,
                            help="include field <%s> in output" % field)

    parser.add_argument('--count', action='store_const', const=True,
                        default=False, help="Show number of Zettels matching this search")
    parser.add_argument('--prompt', action='store_const', const=True,
                        default=False, help="enter query interactively (overrides --input))")
    parser.add_argument('--query', help="load query from file", default=None)
    parser.add_argument(
        '--save-query', help="save source query to file", default=None)
    parser.add_argument(
        '--save-sql', help="save compiled SQL to file (for developers only)", default=None)
    return parser


def main():
    parser = get_argparse()
    args = parser.parse_args()

    # If there is a query file, it overrides all of the other options.
    argsd = vars(args)
    if args.prompt:
        input_line = input("zquery> ")

    elif args.query:
        with open(args.query) as infile:
            input_line = infile.read()

    if input_line:
        ast = zquery.compile(input_line)
        db = zdb.get(args.database)
        gen = db.fts_query(ast)
        if args.save_query:
            if args.save_query != args.query:
                with open(args.save_query, "w") as outfile:
                    outfile.write(input_line)
            else:
                print(
                    "Ignored --save-query as it would clobber existing input file %s" % args.query)
        if args.save_sql:
            with open(args.save_sql, "w") as outfile:
                outfile.write(ast)

    search_count = 0
    printed_something = False
    for row in gen:
        if printed_something:
            print("-" * 3)
        search_count = search_count + 1
        printed_something = False
        if args.use_index:
            z = None
        else:
            loader = zettel.ZettelLoader(row['filename'])
            zettels = loader.getZettels()
            z = next(zettels)

        for field in row.keys():
            show_field = "show_" + field
            if argsd.get(show_field, None):
                if row[field]:
                    if args.verbatim:
                        print(row[field])
                    elif z:
                        print(z.get_yaml([field]))
                    else:
                        print(zettel.dict_as_yaml({field: row[field]}))
                    printed_something = True

    if args.count:
        if printed_something:
            print("-" * 3)
        doc = {'count': search_count, 'query': input_line}
        print(zettel.dict_as_yaml(doc))


if __name__ == '__main__':
    main()
