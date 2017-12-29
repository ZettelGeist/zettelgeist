import sys
import argparse
import os
import os.path
import yaml
from time import strftime

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

        parser.add_argument('--context-%s' % field,
                            type=int, default=32,
                            help="Set context width for field %s (default 32)" % field)

    parser.add_argument(
        '--count', action='store_const', const=True, default=False,
        help="Show number of Zettels matching this search")

    parser.add_argument(
        '--prompt', action='store_const', const=True, default=False,
        help="enter query interactively (overrides --input))")

    parser.add_argument(
        '--query',
        help="load query from file", default=None)

    parser.add_argument(
        '--save-query',
        help="save source query to file", default=None)

    parser.add_argument(
        '--trace-sql',
        help="log all SQL statements used to file", default=None)

    parser.add_argument(
        '--save-sql',
        help="save compiled SQL to file (for developers only)", default=None)

    parser.add_argument(
        '--output',
        help="add text to output filename", default="zfind")

    return parser


def write_data(filename, mode, comment, statement):
    if not filename:
        return
    with open(filename, mode) as outfile:
        outfile.write("\n".join([comment, statement]) + "\n\n")


def counter():
    i = 0
    while True:
        yield i
        i = i + 1


def offsets_gen(int_offsets):
    iterations = len(int_offsets) // 4
    #print(int_offsets, len(int_offsets), iterations)
    offsets_iter = iter(int_offsets)
    for i in range(0, iterations):
        (column, term, pos, size) = int_offsets[i * 4:i * 4 + 4]
        yield {'column': column,
               'term': term,
               'pos': pos,
               'size': size}


def process_offsets(text, offsets, context=100):
    int_offsets = [int(offset) for offset in offsets.split()]
    results = []
    for info in offsets_gen(int_offsets):
        pos = info['pos']
        offset = info['size']
        low_pos = max(pos - offset - context, 0)
        high_pos = min(pos + offset + context, len(text))
        results.append("[[")
        results.append(text[low_pos:high_pos])
        results.append("]]")

    return results


def main():
    parser = get_argparse()
    args = parser.parse_args()
    argsd = vars(args)

    output_dir = strftime("%Y%m%d%H%M%S") + "-%s" % args.output
    if os.path.exists(output_dir):
        print("Please remove directory %s. This error should never happen." % output_dir)
        sys.exit(1)

    try:
        os.mkdir(output_dir)
    except:
        print("Failed to create %s. Please check permissions to write this folder." % output_dir)
        sys.exit(2)

    if args.prompt:
        input_line = input("zquery> ")

    elif args.query:
        with open(args.query) as infile:
            input_line = infile.read()
    else:
        print("No query to process: Use --prompt or --query")
        return
    print("zfind writing results to folder %s" % output_dir)

    (ast2, semantics2) = zquery.compile2(input_line)
    db = zdb.get(args.database)
    gen = None
    for statement in [semantics2.sql_drop_matches_table(), semantics2.sql_create_matches_table(ast2)]:
        write_data(args.trace_sql, "a", "", statement)
        gen = db.fts_query(statement)
        for g in gen:
            pass

    select_sql = semantics2.sql_get_matches()
    search_result_generator = db.fts_query(select_sql)

    write_data(args.trace_sql, "a", "# query match", select_sql)
    write_data(args.save_query, "w", "", input_line)
    write_data(args.save_sql, "w", "", ast2)
    write_data(args.trace_sql, "a", "# saved SQL query", ast2)

    search_counter = counter()
    results_counter = counter()

    search_count = next(search_counter)
    snippets_count = 0

    search_result_generator = db.fts_query(select_sql)
    # TODO: Investigated nested cursor issue
    # Temporary workaround is to force evaluation of outer generator (not nice)

    current_time = strftime("%Y%m%d%H%M%S")
    all_results = list(search_result_generator)
    format_d_length = len(str(len(all_results)))
    match_filenames = []
    for search_result in all_results:
        docid = search_result['docid']
        suffix_format = "-%%0%dd.yaml"
        filename = current_time + (suffix_format %
                                   format_d_length) % search_count
        print("... " + filename)
        output_path = os.path.join(output_dir, filename)

        outfile = open(output_path, "w")
        bound_query = "SELECT *,docid from zettels where docid = %(docid)s" % vars(
        )
        write_data(args.trace_sql, "a",
                   "# finding zettels by docid", bound_query)

        search_details_generator = db.fts_query(bound_query)
        try:
            row = next(search_details_generator)
        except:
            print("Unexpected end of iteration")

        match_filenames.append(row['filename'])

        z = None
        if not args.use_index:
            loader = zettel.ZettelLoader(row['filename'])
            zettels = loader.getZettels()
            z = next(zettels)

        for field in zettel.ZettelFields:
            show_field = "show_" + field
            context_field = "context_" + field
            if argsd.get(show_field, None):
                for query in semantics2.get_field_query_sql(field, argsd[context_field], docid):
                    field_query_generator = db.fts_query(query)
                    write_data(args.trace_sql, "a", "", query)
                    for result in field_query_generator:
                        if query.find("offsets(") >= 0:
                            snippets = process_offsets(
                                result[field + "_verbatim"], result[field + "_offsets"])
                            snippets_count = snippets_count + len(snippets)
                            outfile.write(zettel.dict_as_yaml(
                                {field: "\n".join(snippets)}) + "\n")
                        elif result[field]:
                            if z:
                                outfile.write(z.get_yaml([field]) + "\n")
                            else:
                                outfile.write(zettel.dict_as_yaml(
                                    {field: result[field]}) + "\n")

        # TODO: Allow filename to be kept in the Zettel. Should be possible but we would just never save it.
        # Would like to eliminate special case code like the following to eliminate duplication.

        if argsd.get("show_filename"):
            for query in semantics2.get_field_query_sql('filename', 32768, docid):
                write_data(args.trace_sql, "a", "", query)
                field_query_generator = db.fts_query(query)

                for result in field_query_generator:
                    outfile.write(zettel.dict_as_yaml(
                        {"filename": result["filename"]}) + "\n")

        search_count = next(search_counter)
        outfile.close()

    if False:
        drop_temp_matches_table = semantics2.sql_drop_matches_table()
        write_data(args.trace_sql, "a", "", drop_temp_matches_table)
        gen = db.fts_query(drop_temp_matches_table)
        for g in gen:
            pass

    if args.count:
        filename = current_time + "-stats.yaml"
        output_path = os.path.join(output_dir, filename)
        doc = {'count': search_count,
               'snippets_count': snippets_count, 'query': input_line.strip()}
        with open(output_path, "w") as outfile:
            outfile.write(zettel.dict_as_yaml(doc) + "\n")

        filename = current_time + "-fileset.txt"
        output_path = os.path.join(output_dir, filename)
        with open(output_path, "w") as outfile:
            match_filenames = list(set(match_filenames))
            outfile.write("\n".join(match_filenames) + "\n")     

if __name__ == '__main__':
    main()
