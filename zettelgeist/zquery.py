import sys
import readline
import pprint
import json
import tatsu
import argparse
import os.path

from zettelgeist import zdb, zettel

def parse_options():
    parser = argparse.ArgumentParser()
    parser.add_argument('--prompt', action='store_const', const=True,
                        default=False, help="enter query interactively (overrides --input))")
    parser.add_argument('--input', help="load query from file", default=None)
    parser.add_argument('--output', help="save compiled query for use with zfind.py", default=None)
    return parser.parse_args()

def unquote(text):
    return text.replace('"','').replace("'","")

class ZG(object):
    def literal(self, ast):
        return ast.word

    def _get_match_clause(self, ast, negate):
        text = unquote(ast.text)
        words = text.split()
        return " NEAR/1 ".join([ "%s%s:%s" % (negate,ast.field,word) for word in words ])
    def z_field(self, ast):
        match_clause = self._get_match_clause(ast,'')
        return "SELECT * FROM zettels WHERE zettels MATCH '%s'" % match_clause

    def nz_field(self, ast):
        match_clause = self._get_match_clause(ast,'-')
        return "SELECT * FROM zettels WHERE zettels MATCH '%s'" % match_clause

    def and_expr(self, ast):
        return "SELECT * from (%s INTERSECT %s)" % (ast.left, ast.right)

    def or_expr(self, ast):
        return "SELECT * from (%s UNION %s)" % (ast.left, ast.right)

def main():
    #grammar = open('zquery.ebnf').read()
    parser = tatsu.compile(zdb.GRAMMAR)

    args = parse_options()
    input_line = None

    if args.prompt:
        input_line = input("zquery> ")

    elif args.input:
        with open(args.input) as infile:
            input_line = infile.read()

    if input_line:
        ast = parser.parse(input_line, semantics=ZG())
        if args.output:
            query_filename = ".".join([args.output, 'zq'])
            compiled_filename = ".".join([args.output, 'sql'])
            if os.path.exists(query_filename):
                os.rename(query_filename, ".".join([query_filename, 'orig']))
            with open(compiled_filename, "w") as outfile:
                outfile.write(ast + "\n")
            with open(query_filename, "w") as outfile:
                outfile.write(input_line)
        else:
            print(ast)


if __name__ == '__main__':
    main()
