import sys
import readline
import pprint
import json
import tatsu

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

if __name__ == '__main__':
    grammar = open('zquery.ebnf').read()
    parser = tatsu.compile(grammar)

    sys.stderr.write("Enter a query, and I will check it's syntax\n")
    sys.stderr.write("""e.g. >> title:Charles | title:Babbage | text:George & -text:Bob & -note:"Sir Charles"\n """)
    input_line = input()
    ast = parser.parse(input_line, semantics=ZG())
    print(ast)
