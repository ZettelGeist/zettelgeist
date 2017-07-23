#
# zettel.py - A checker for Zettels
#

import sys
import argparse
import yaml
from zettelgeist import zdb

# Recursive descent parsing of Zettel dictionary format.

ZettelStringFields = ['title', 'bibkey', 'bibtex',
                      'ris', 'inline', 'url', 'summary', 'comment', 'note']
ZettelListFields = ['tags', 'mentions']
ZettelStructuredFields = ['cite', 'dates']
ZettelFieldsOrdered = ZettelStringFields + \
    ZettelListFields + ZettelStructuredFields
ZettelFields = set(ZettelFieldsOrdered)
CitationFields = set(['bibkey', 'page'])
DatesFields = set(['year', 'era'])


class ParseError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


def typename(value):
    return type(value).__name__


def parse_zettel(doc):
    if not isinstance(doc, dict):
        raise ParseError(
            "Zettels require key/value mappings at top-level. Found %s" % typename(doc))

    parse_check_zettel_field_names(doc)

    # These fields are all optional but, if present, must be strings
    parse_string_field(doc, 'title')
    parse_string_field(doc, 'bibkey')
    parse_string_field(doc, 'bibtex')
    parse_string_field(doc, 'ris')
    parse_string_field(doc, 'inline')
    parse_string_field(doc, 'url')
    parse_string_field(doc, 'summary')
    parse_string_field(doc, 'comment')
    parse_string_field(doc, 'note')

    # These fields are all optional but, if present, must be list of strings

    parse_list_of_string_field(doc, 'tags')
    parse_list_of_string_field(doc, 'mentions')

    parse_citation(doc, 'cite')
    parse_dates(doc, 'dates')

    # TODO: Check for extraneous fields in all cases


def parse_check_zettel_field_names(doc):
    check_field_names(doc, ZettelFields, "Zettel")


def parse_check_citation_field_names(doc):
    check_field_names(doc, CitationFields, "Citation")


def parse_check_dates_field_names(doc):
    check_field_names(doc, DatesFields, "Dates")


def check_field_names(doc, name_set, label):
    for key in doc.keys():
        if key not in name_set:
            raise ParseError("Invalid field %s found in %s" % (key, label))


def parse_string_field(doc, field, required=False):
    value = doc.get(field, None)
    if value == None:
        if required:
            raise ParseError("Field %s requires a string but found %s of type %s" % (
                field, value, typename(value)))
        return
    if not isinstance(value, str):
        raise ParseError("Field %s must be a string or not present at all - found value %s of type %s" %
                         (field, value, typename(value)))


def parse_list_of_string_field(doc, field, required=False):
    value = doc.get(field, None)
    if value == None:
        if required:
            raise ParseError("Field %s requires a list of strings" % field)
        return
    if not isinstance(value, (list, tuple)):
        raise ParseError("Field %s must be a list or not present at all - foudn value %s of type %s" %
                         (field, value, typename(value)))

    # Make a dictionary of the list items for checking purposes only
    # That is, treat the list like a dictionary. Will simplify with comprehension magic later
    doc2 = {}
    pos = 0
    for item in value:
        doc2["%s(%d)" % (field, pos)] = item
    for key in doc2.keys():
        parse_string_field(doc2, key, True)


def parse_citation(doc, field):
    value = doc.get(field, None)
    if value == None:
        return
    if not isinstance(value, dict):
        raise ParseError("%s must be a nested (citation) dictoinary" % field)
    parse_check_citation_field_names(value)
    parse_string_field(value, 'bibkey', True)
    parse_string_field(value, 'page')


def parse_dates(doc, field):
    value = doc.get(field, None)
    if value == None:
        return
    if not isinstance(value, dict):
        raise ParseError("%s must be a nested (dates) dictionary" % field)
    parse_check_dates_field_names(value)
    parse_string_field(value, 'year', True)
    parse_string_field(value, 'era')

# This is to support formatting of resulting YAML (after modification of the underlying dictionary)


# Credit to StackOverflow for helping figure out how to format YAML
# multiline strings properly (when emitting YAML representation of Zettel)

from collections import OrderedDict


class quoted(str):
    pass


class literal(str):
    pass


def quoted_presenter(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')

# Note: Only use multiline syntax when there are actually multiple lines.


def str_presenter(dumper, data):
    if len(data.splitlines()) > 1:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)


def ordered_dict_presenter(dumper, data):
    return dumper.represent_dict(data.items())


class ZettelBadKey(Exception):
    def __init__(self, name):
        self.name = name


class ZettelStringRequired(Exception):
    def __init__(self, value):
        self.value = value


def get_argparse():
    parser = argparse.ArgumentParser()
    for field in ZettelStringFields:
        parser.add_argument('--set-%s' %
                            field, help="set the value of field %s" % field)
        parser.add_argument('--delete-%s' % field, action="store_true",
                            help="delete field %s" % field, default=False)
        parser.add_argument('--load-%s' %
                            field, help="load field from %s" % field)

    for field in ZettelListFields:
        parser.add_argument('--reset-%s' % field, action="store_true",
                            help="reset list field %s" % field, default=False)
        parser.add_argument('--remove-entries-in-%s' % field, nargs=2, metavar=('FASS ENTRY', 'LIST ENTRY'), type=str,
                            help="delete comma-separated LIST ENTRY positions from FASS ENTRY")
        parser.add_argument('--append-%s' %
                            field, nargs="+", help="add value to list field %s" % field)


    parser.add_argument('--set-citation', nargs='+', type=str,
            help="set citation - first arg is bibkey, rest are page numbers or ranges (no commas), e.g. Turing1936 ii-iv 36 1-25")

    parser.add_argument('--file', nargs='?',
                        help='Zettel files (.yaml) to process')
    return parser


def flatten(item):
    if item == None:
        return [""]
    elif isinstance(item, dict):
        return flatten([":".join([k, item[k]]) for k in item])
    elif not isinstance(item, (tuple, list)):
        return [str(item)]

    if len(item) == 0:
        return item
    else:
        return flatten(item[0]) + flatten(item[1:])


class Zettel(object):

    def __init__(self, data={}):
        self.zettel = data
        parse_zettel(self.zettel)

    def set_field(self, name, value):
        self.zettel[name] = value
        parse_zettel(self.zettel)

    def delete_field(self, name):
        del(self.zettel[name])
        parse_zettel(self.zettel)

    def reset_list_field(self, name):
        self.zettel[name] = []
        parse_zettel(self.zettel)

    def delete_list_field_entries(self, name, positions):
        if name not in self.zettel:
            return
        positions.sort(reverse=True)
        for position in positions:
            del(self.zettel[name][position])
        if len(self.zettel[name]) == 0:
            del(self.zettel[name])

    def append_list_field(self, name, value):
        self.zettel[name] = self.zettel.get(name, [])
        self.zettel[name].append(value)
        parse_zettel(self.zettel)

    def set_citation(self, bibkey, page=None):
        citation = {'bibkey': bibkey}
        if page != None:
            citation['page'] = page
        self.zettel['cite'] = citation
        parse_zettel(self.zettel)

    def set_dates(self, year, era=None):
        dates = {'year': year}
        if era != None:
            dates['era'] = era
        self.zettel['dates'] = dates
        parse_zettel(self.zettel)

    def load_field(self, name, filename):
        text = []
        with open(filename, 'r') as infile:
            text = infile.readlines()
        self.set_field(name, ''.join(text))
        parse_zettel(self.zettel)

    def get_yaml(self):
        yaml.add_representer(quoted, quoted_presenter)
        yaml.add_representer(literal, str_presenter)
        yaml.add_representer(OrderedDict, ordered_dict_presenter)
        parse_zettel(self.zettel)
        yaml_zettel = OrderedDict()
        for key in ZettelFieldsOrdered:
            if key not in self.zettel:
                continue
            if key in ZettelStringFields:
                yaml_zettel[key] = literal(self.zettel[key])
            else:
                yaml_zettel[key] = self.zettel[key]
        return yaml.dump(yaml_zettel, default_flow_style=False)

    def get_indexed_representation(self):
        parse_zettel(self.zettel)
        return {key: ",".join(flatten(self.zettel[key])) for key in self.zettel}

#
# This generic loader can be used in any module that needs to work on a Fass or Stein
# Will be used mainly by zimport.py
#


class ZettelLoaderError(Exception):
    def __init__(self, message):
        self.message = message


class ZettelLoader(object):
    def __init__(self, filename):
        with open(filename) as infile:
            try:
                text = infile.read()
            except:
                raise ZettelLoaderError(
                    "%s: I/O error - Encoding must be UTF-8" % filename)
        try:
            self.ydocs = yaml.load_all(text)
        except:
            raise ZettelLoaderError("%s: YAML load failure" % filename)

    def getZettels(self):
        for ydoc in self.ydocs:
            if isinstance(ydoc, dict):
                yield Zettel(ydoc)


def main():
    parser = get_argparse()
    args = parser.parse_args()
    z_generator = gen_new_zettels(args)
    print("---\n".join([z.get_yaml() for z in z_generator]))


def gen_id():
    id = 0
    while True:
        yield id
        id = id + 1

def gen_new_zettels(args):
    vargs = vars(args)
    id_gen = gen_id()
    if args.file:
        loader = ZettelLoader(args.file)
        for z in loader.getZettels():
            yield process_zettel_command_line_options(z, vargs, next(id_gen))
    else:
        yield process_zettel_command_line_options(Zettel(), vargs, next(id_gen))

def process_zettel_command_line_options(z, vargs, id):
    for arg in vargs:
        if arg.startswith("reset_"):
            reset_what = arg[len("reset_"):]
            if vargs[arg]:
                z.reset_list_field(reset_what)

        if arg.startswith("delete_"):
            delete_what = arg[len("delete_"):]
            if vargs[arg]:
                z.delete_field(delete_what)

        if arg.startswith("remove_entries_in_"):
            delete_what = arg[len("remove_intries_in_"):]
            if vargs[arg]:
                try:
                   (zettel_id, list_entries) = vargs[arg][:2]
                   zettel_id = int(zettel_id)
                   list_entries = [int(pos) for pos in list_entries.split(",")]
                except:
                   print("Non-integer zettel ID or list position found in %s. Aborting." % arg)
                   sys.exit(1)
                if id == zettel_id:
                   z.delete_list_field_entries(delete_what, list_entries)


    for arg in vargs:
        if arg == "set_citation":
            cite_info = vargs[arg]
            bibkey = cite_info[0]
            try:
                pages = ",".join(cite_info[1:])
            except:
                pass
            z.set_citation(bibkey, pages)
        elif arg == "set_dates":
            pass

        elif arg.startswith("set_"):
            set_what = arg[len("set_"):]
            if vargs[arg]:
                # TODO: Make replacement of literal \n with newline an option
                value = vargs[arg].replace(r"\n", "\n")
                z.set_field(set_what, value)

        if arg.startswith("append_"):
            append_what = arg[len("append_"):]
            if vargs[arg]:
                for text in vargs[arg]:
                    z.append_list_field(append_what, text)

        if arg.startswith("load_"):
            load_what = arg[len("load_"):]
            if vargs[arg]:
                z.load_field(load_what, vargs[arg])

    return z


if __name__ == '__main__':
    main()
