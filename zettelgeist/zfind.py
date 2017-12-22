import sys
import argparse
import yaml
from . import zdb, zettel, zquery


def get_argparse():
    parser = zdb.get_argparse()
    parser.add_argument('--use-index', action='store_const',
                        const=True, default=False)

    for field in zdb.ZettelSQLFields:
        # parser.add_argument('--find-%s' %
        #                    field, help='search the Zettel %s field' % field)
        # parser.add_argument('--exclude-%s' %
        #                    field, help='search the Zettel %s field' % field)
        parser.add_argument('--show-%s' % field,
                            action='store_const', const=True, default=False,
                            help="include field <%s> in output" % field)
        parser.add_argument('--snip-count-%s' % field, type=int, default=100, help="Set snip width for field %s (defaults to 100)" % field)

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
        (ast, semantics) = zquery.compile(input_line)
        (ast2, semantics2) = zquery.compile2(
            input_line)  # This duplication is temporary
        db = zdb.get(args.database)
        gen = None
        for statement in semantics2.get_create_sql(ast2):
            #print("executing", statement)
            gen = list(db.fts_query(statement))

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
    for outer in gen:
        inner_gen = db.fts_query(
            "SELECT *,docid from zettels where docid = %s" % outer['docid'])
        
        # no loop for this generator, because it only returns one row
        row = next(inner_gen)
        #print(">>> RESULT ROW/%s" % outer['docid'])

        if printed_something:
            print("-" * 3)

        if args.use_index:
            z = None
        else:
            loader = zettel.ZettelLoader(row['filename'])
            zettels = loader.getZettels()
            z = next(zettels)

        for field in zettel.ZettelFields:
            show_field = "show_" + field
            snip_field = "snip_" + field
            if argsd.get(show_field, None):
                for query in semantics2.get_field_query_sql(field):
                    rgen = db.fts_query(query % row['docid'])
                    #print(">> SQL-standard-fields/%s" % field, query % row['docid'])
                    for result in rgen:
                        if result[field]:
                            if z:
                                print(z.get_yaml([field]))
                            else:
                                print(zettel.dict_as_yaml(
                                    {field: result[field]}))
                            printed_something = True

            # if argsd.get(snip_field, None):
            #    for query in semantics2.get_field_query_sql(field):
            #    	print(">> MATCH QUERY %s" % field, query % row['docid'])

        if argsd.get("show_filename"):
            for query in semantics2.get_field_query_sql('filename'):
                #print(">> SQL-filename/%s" % field, query % row['docid'])
                rgen = db.fts_query(query % row['docid'])
                for result in rgen:
                    print(zettel.dict_as_yaml(
                        {"filename": result["filename"]}))
                    printed_something = True

        # The filename is a special case as it is not stored in the Zettel
        # Might rethink this at some point.

        search_count = search_count + 1

    if args.count:
        if printed_something:
            print("-" * 3)
        doc = {'count': search_count, 'query': input_line}
        print(zettel.dict_as_yaml(doc))


if __name__ == '__main__':
    main()
