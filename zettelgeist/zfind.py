import sys
import argparse
from time import strftime
import yaml

from . import zdb, zettel, zquery
from .zutils import *

YAML_HEADER = '---'

def get_argparse():
    parser = zdb.get_argparse()

    for field in zdb.ZettelSQLFields:
        parser.add_argument('--show-%s' % field,
                            action='store_const', const=True, default=False,
                            help="include field <%s> in output" % field)

    parser.add_argument('--count', action='store_const', const=True,
                        default=False, help="Show number of Zettels matching this search")

    parser.add_argument(
        '--query-prompt', action='store_const', const=True, default=False,
        help="prompt for ZQL query (overrides --query-string, --query-file))")

    parser.add_argument(
        '--query-file', help="load ZQL query from file (overrides --query)", default=None)

    parser.add_argument(
        '--query-string',
        help="load ZQL from string", default=None)

    parser.add_argument(
        '--fileset', help="write fileset to filename", default=None)

    parser.add_argument(
        '--stats', help="write statistics and parameters to filename", default=None)

    parser.add_argument(
        '--get-all-tags', help="show all tags in this database (disables all other options)", action="store_true", default=False)

    parser.add_argument(
        '--get-all-mentions', help="show all mentions in this database (disables all other options)", action="store_true", default=False)

    return parser


def main():
    parser = get_argparse()
    args = parser.parse_args()
    argsd = vars(args)

    db = zdb.get(args.database)

    # The --get-all-tags and --get-all-mentions stop processing of all other tags
    # TODO: Make each group of functions a function to make this more comprehensible.

    if args.get_all_tags:
        print('\n'.join(db.get_tags_list()))
        exit(0)

    if args.get_all_mentions:
        print('\n'.join(db.get_mentions_list()))
        exit(0)

    # The --query-{prompt,file,string} options are for ZQL processing.

    if args.query_prompt:
        input_line = input("zfind> ")
    elif args.query_file:
        with open(args.query_file) as infile:
            input_line = infile.read()
    elif args.query_string:
        input_line = args.query_string
    else:
        print("No query option (--query-string, --query-file, or --query-prompt) found")
        return

    if input_line:
        ast = zquery.compile(input_line)
        gen = db.fts_query(ast[0])
    else:
        print("Warning: Query could not be loaded via --query, --query-file, or --query-prompt")
        sys.exit(1)

    # This is the actual logic to find and process results.

    search_count = 0
    match_filenames = []
    for row in gen:
        search_count = search_count + 1
        printed_something = False
        match_filenames.append(row['filename'])
        loader = zettel.ZettelLoader(row['filename'])
        zettels = loader.getZettels()
        z = next(zettels)

        # Handle output of YAML here
        this_result_output = []
        for field in row.keys():
            show_field = "show_" + field
            if show_field == 'show_filename':
                filename_yaml = yaml.dump({ 'filename' : row['filename']})
                this_result_output.append(filename_yaml.rstrip())
            elif show_field == 'show_document':
                continue
            elif argsd.get(show_field, None):
                if row[field]:
                    if z:
                        this_result_output.append(z.get_yaml([field]).rstrip())
                    else:
                        this_result_output.append("%s:" % field)
                        this_result_output.append(row[field])

        # No output if just --- and ---
        if len(this_result_output) > 0:
           print('\n'.join([YAML_HEADER] + this_result_output + [YAML_HEADER]))

        if argsd.get("show_document"):
            document = row['document']
            if len(document) > 0:
                print(row['document'])
                print()

    # --count here / Should this be added to the YAML payload? I think the answer is yes.

    if args.count:
        print("%d Zettels matched search" % search_count)

    # --fileset handled here / Should --fileset actually suppress the --show options? 
    # It's primary purpose is to *avoid* showing output for subsequent processing, say, in a shell loop

    if args.fileset:
        if not os.path.exists(args.fileset):
           write_to_file(args.fileset, "\n".join(match_filenames), mode="w", newlines=1)
        else:
           print("Filename %s exists; will not overwrite." % args.fileset)

    # --stats seems to duplicate the work of --count. yes, it goes to a file, but that would
    # allow for subsequent querying, say, with yq or equivalent.

    if args.stats:
        if not os.path.exists(args.stats):
           doc = {'count': search_count, 'query': input_line.strip()}
           write_to_file(args.stats, zettel.dict_as_yaml(doc), mode="w", newlines=1)
        else:
           print("Filename %s exists; will not overwrite." % args.stats)

if __name__ == '__main__':
    main()
