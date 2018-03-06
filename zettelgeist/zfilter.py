import sys
import argparse
import re
import os
import os.path
import yaml
from time import strftime

from . import zdb, zettel, zquery


def get_argparse():
    parser = zdb.get_argparse()

    for field in zettel.ZettelFieldsOrdered:
        parser.add_argument('--show-%s' % field,
                            action='store_const', const=True, default=False,
                            help="include field <%s> in output" % field)

    parser.add_argument(
        '--count', action='store_const', const=True, default=False,
        help="write number of zettels matched to statistics file")

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
        help="add text to output folder name", default="zfilter")

    parser.add_argument(
        '--snip-size',
        help="snippet size", type=int, default=2500)

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


def offsets_gen(int_offsets, text):
    iterations = len(int_offsets) // 4
    for i in range(0, iterations):
        (column, term, pos, size) = int_offsets[i * 4:i * 4 + 4]
        yield {'column': column,
               'term': term,
               'pos': pos,
               'size': size,
               'substring': text[pos:pos + size]}


def process_offsets(filename, text, offsets, context):
    int_offsets = [int(offset) for offset in offsets.split()]
    results = []

    previous = (len(text), 0)
    for info in offsets_gen(int_offsets, text):
        pos = info['pos']
        offset = info['size']
        low_pos = max(pos - offset - context, 0)
        high_pos = min(pos + offset + context, len(text))
        if pos >= previous[0] and pos + offset <= previous[1]:
           #print("skipping already output snippet [%d,%d]" % (pos, offset))
           continue
        else:
           previous = (low_pos, high_pos)
        #print("match @ [%s,%d] - snippet at [%d,%d]" % (pos, offset, low_pos, high_pos))
        results.append(text[low_pos:high_pos])
    return results


def write_to_file(filepath, text, **kwargs):
    mode = kwargs.get("mode", "a")
    newlines = kwargs.get("newlines", 1)
    with open(filepath, mode) as outfile:
        outfile.write(text)
        if newlines:
            outfile.write("\n" * int(newlines))


def get_context(snip):
    text = snip.strip()
    ws_matches = list(re.finditer("\s+", text))
    if len(ws_matches) < 2:
        return text

    first = ws_matches[0].end()
    last = ws_matches[-1].start()
    return text[first:last]


# TODO Create zutils.py module

def dirname(path):
    return os.path.split(path)[0]


def basename(path):
    return os.path.split(path)[1]


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

    write_data(args.trace_sql, "a", "# query match", select_sql)
    write_data(args.save_query, "w", "", input_line)
    write_data(args.save_sql, "w", "", ast2)
    write_data(args.trace_sql, "a", "# saved SQL query", ast2)

    search_counter = counter()

    search_count = next(search_counter)
    snippets_count = 0

    search_result_generator = db.fts_query(select_sql)

    current_time = strftime("%Y%m%d%H%M%S")
    all_results = list(search_result_generator)
    format_d_length = len(str(len(all_results)))
    match_filenames = []
    for search_result in all_results:
        docid = search_result['docid']
        base_name = current_time + ("-%%0%dd" % format_d_length) % search_count
        base_path = os.path.join(output_dir, base_name)
        yaml_path = base_path + '.yaml.in'

        print("... " + basename(yaml_path))

        write_to_file(
            yaml_path, "# Note: This is a generated .yaml.in file intended for editing (editor or zettel command)", mode="w", newlines=0)

        bound_query = "SELECT *,docid from zettels where docid = %(docid)s" % vars(
        )
        write_data(args.trace_sql, "a",
                   "# finding zettels by docid", bound_query)

        search_details_generator = db.fts_query(bound_query)
        try:
            row = next(search_details_generator)
        except:
            print("Unexpected end of iteration")

        current_filename = row['filename']
        match_filenames.append(current_filename)

        write_to_file(yaml_path, "# zfind search results",
                      mode="a", newlines=1)
        write_to_file(yaml_path, "# filename = %s" %
                      current_filename, mode="a", newlines=1)
        write_to_file(yaml_path, "# query = %s" %
                      input_line.strip(), mode="a", newlines=2)

        try:
            loader = zettel.ZettelLoader(row['filename'])
            zettels = loader.getZettels()
            z = next(zettels)
        except:
            print("Warning: Cannot load source Zettel %s from filesystem (using database instead)" %
                  row['filename'])
            z = None

        snips_written = set()
        snip_size = max(args.snip_size, 250)
        for field in zettel.ZettelFields:
            show_field = "show_" + field
            if argsd.get(show_field, None):
                for query in semantics2.get_field_query_sql(field, snip_size, docid):
                    field_query_generator = db.fts_query(query)
                    write_data(args.trace_sql, "a", "", query)
                    for result in field_query_generator:
                        if query.find("offsets(") >= 0:
                            #print("Processing offsets for %s" % field)
                            snippets = process_offsets(current_filename,
                                                       result[field + "_verbatim"], result[field + "_offsets"], snip_size)
                            snippets_count = snippets_count + len(snippets)

                            # Write text version
                            snip_path = base_path + '-%s.txt' % field

                            for snip in snippets:
                                write_to_file(snip_path, "# filename = %s" %
                                              current_filename, mode="a", newlines=1)
                                write_to_file(snip_path, "# field = %s" %
                                              field, mode="a", newlines=2)
                                write_to_file(snip_path, snip, mode="a", newlines=2)

                            snip_id = ":".join([snip_path, field])
                            if snip_id not in snips_written:
                                write_to_file(yaml_path,
                                              "# %s -> See %s for snippets." % (field, snip_path), mode="a", newlines=2)
                                snips_written.add(snip_id)

                        elif result[field]:
                            write_to_file(yaml_path, z.get_yaml(
                                [field]), mode="a", newlines=1)

        search_count = next(search_counter)

    if False:
        drop_temp_matches_table = semantics2.sql_drop_matches_table()
        write_data(args.trace_sql, "a", "", drop_temp_matches_table)
        gen = db.fts_query(drop_temp_matches_table)
        for g in gen:
            pass

    if args.count:
        stats_path = base_path + '-stats.yaml'
        files_path = base_path + '-fileset.yaml'

        doc = {'count': search_count,
               'query': input_line.strip()}

        write_to_file(stats_path, zettel.dict_as_yaml(
            doc), mode="w", newlines=1)
        write_to_file(files_path, "\n".join(
            match_filenames), mode="w", newlines=1)


if __name__ == '__main__':
    main()
