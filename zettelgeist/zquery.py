import pprint
import json
import tatsu

class ZG(object):
    def literal(self, ast):
        return ast.word

    def z_field(self, ast):
        return "%s:%s" % (ast.field, ast.text)

    def nz_field(self, ast):
        return "-%s:%s" % (ast.field, ast.text)

    def and_expr(self, ast):
        return "(%s AND %s)" % (ast.left, ast.right)

    def or_expr(self, ast):
        return "(%s OR %s)" % (ast.left, ast.right)

if __name__ == '__main__':
    grammar = open('zquery.ebnf').read()
    parser = tatsu.compile(grammar)

    ast = parser.parse('title:Charles | title:Babbage | text:George & -text:Bob & -note:"Sir Charles as phrase"', semantics=ZG())
    print('# PPRINT')
    pprint.pprint(ast, indent=2, width=70)
    print()

    print('# JSON')
    print(json.dumps(ast, indent=2))
    print()
