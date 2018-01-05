import sys
import readline
import pprint
import json
import tatsu
import argparse
import os.path
import tempfile
import pprint

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


def get_temp_table_name():
    return os.path.split(tempfile.mktemp())[1]


class ZG2(object):
    def __init__(self, select_fields=["docid"]):
        self.queries = {}
        self.select_fields = ",".join(select_fields)
        self.temp_table_name = get_temp_table_name()
        self.create_temp_table_clause = "CREATE TABLE %s AS %%s" % self.temp_table_name
        self.drop_table_statement = "DROP TABLE IF EXISTS %s" % self.temp_table_name
        self.select_all = "SELECT docid from %s" % self.temp_table_name

    def sql_drop_matches_table(self):
        return self.drop_table_statement

    def sql_create_matches_table(self, compiled_query):
        return self.create_temp_table_clause % compiled_query

    def sql_get_matches(self):
        return self.select_all

    def get_field_query_sql(self, field, field_context, docid):
        default = """SELECT docid, %(field)s FROM zettels WHERE docid = %(docid)s""" % vars(
        )
        field_queries = self.queries.get(field, [default]).copy()
        for i in range(0, len(field_queries)):
            field_queries[i] = field_queries[i] % vars()
        #print(">>> field_queries", field_queries)
        return field_queries

    def literal(self, ast):
        return ast.word

    def _get_match_clause(self, ast, negate):
        text = unquote(ast.text)
        words = text.split()
        return " NEAR/1 ".join(["%s%s:%s" % (negate, ast.field, word) for word in words])

    def z_field(self, ast):
        match_clause = self._get_match_clause(ast, '')
        query_list = self.queries.get(ast.field, [])
        field_query = "SELECT docid FROM zettels WHERE zettels MATCH '%s'" % match_clause
        context_query = """SELECT docid, snippet(zettels, '[', ']', '...', -1, -%%(field_context)s) as %s, %s as %s_verbatim, offsets(zettels) as %s_offsets FROM zettels WHERE zettels MATCH '%s' AND docid = %%(docid)s""" % (
            ast.field, ast.field, ast.field, ast.field, match_clause)
        query_list.append(context_query)
        self.queries[ast.field] = query_list
        return field_query

    def and_expr(self, ast):
        if ast.op == '&':
            return "SELECT %s from (%s INTERSECT %s)" % (self.select_fields, ast.left, ast.right)
        elif ast.op == '!':
            return "SELECT %s from (%s EXCEPT %s)" % (self.select_fields, ast.left, ast.right)
        # else: parser should have caught any non-op

    def and_op(self, ast):
        return ast.op

    def or_expr(self, ast):
        return "SELECT %s from (%s UNION %s)" % (self.select_fields, ast.left, ast.right)


def compile(input_line):
    parser = tatsu.compile(zdb.GRAMMAR)
    zg_semantics = ZG()
    ast = parser.parse(input_line, semantics=zg_semantics)
    return (ast, zg_semantics)


def compile2(input_line):
    parser = tatsu.compile(zdb.GRAMMAR)
    zg_semantics = ZG2()
    ast = parser.parse(input_line, semantics=zg_semantics)
    return (ast, zg_semantics)
