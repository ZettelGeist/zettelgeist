import sys
import readline
import pprint
import json
import tatsu
import argparse
import os.path

from . import zdb, zettel


def unquote(text):
    return text.replace('"', '').replace("'", "")


class ZG(object):
    def literal(self, ast):
        return ast.word

    def _get_match_clause(self, ast, negate):
        text = unquote(ast.text)
        words = text.split()
        return " NEAR/1 ".join(["%s%s:%s" % (negate, ast.field, word) for word in words])

    def z_field(self, ast):
        match_clause = self._get_match_clause(ast, '')
        return "SELECT * FROM zettels WHERE zettels MATCH '%s'" % match_clause

    def and_expr(self, ast):
        if ast.op == '&':
            return "SELECT * from (%s INTERSECT %s)" % (ast.left, ast.right)
        elif ast.op == '!':
            return "SELECT * from (%s EXCEPT %s)" % (ast.left, ast.right)
        # else: parser should have caught any non-op

    def and_op(self, ast):
        return ast.op

    def or_expr(self, ast):
        return "SELECT * from (%s UNION %s)" % (ast.left, ast.right)


def compile(input_line):
    parser = tatsu.compile(zdb.GRAMMAR)
    ast = parser.parse(input_line, semantics=ZG())
    return ast
