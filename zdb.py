 
# ZettelGeist uses a FTS system for organizing Zettels. The index is intended
# to be emphemeral and can be regenerated at any time. The schema itself is
# ephemeral and can be augmented with additional fields of interest.
# 

import sqlite3
import os

ZETTEL_FIELDS=['filename', 'title', 'tags', 'mentions', 'outline', 'cite', 'dates', 'summary', 'text', 'bibkey', 'bibtex', 'ris', 'inline', 'note', 'url' ]

# This is for showing data structures only.

import pprint
printer = pprint.PrettyPrinter(indent=2)

#
# Flattens a list of text. Any item not text is converted to text forcibly,
# if necessary.
#

def flatten(item):
    if item == None:
        return [""]
    if type(item) != type([]):
        return [str(item)]
    if len(item) == 0:
        return item
    else:
        return flatten(item[0]) + flatten(item[1:])

def unquote(text):
   return text.replace('"','').replace("'","")

class SQLiteFTS(object):  
  def __init__(self, db_name, table_name, field_names):
    self.db_name = db_name
    self.conn = sqlite3.connect(db_name)
    self.conn.row_factory = sqlite3.Row
    self.cursor = self.conn.cursor()
    
    self.table_name = table_name
    self.fts_field_names = field_names
    self.fts_field_refs = ['?'] * len(self.fts_field_names)  # for sqlite insert template generation
    self.fts_field_init = [''] * len(self.fts_field_names)
    self.fts_fields = dict(zip(self.fts_field_names, self.fts_field_refs))
    self.fts_default_record = dict(zip(self.fts_field_names, self.fts_field_init))

  def bind(self, doc):
    self.record = self.fts_default_record.copy()
    for k in doc.keys():
        if k in self.record.keys():
           if doc[k] != None: self.record[k] = doc[k]
        else:
           print("Unknown fts field %s - deleting it" % k)
           
    #self.record.update(doc)
    
  def drop_table(self):
    self.cursor.execute("DROP TABLE IF EXISTS %s" % self.table_name)
    self.conn.commit()

  def create_table(self):
    sql_fields = ",".join(self.fts_default_record.keys())
    #print("CREATE VIRTUAL TABLE zettels USING fts4(%s)" % sql_fields)
    self.cursor.execute("CREATE VIRTUAL TABLE zettels USING fts4(%s)" % sql_fields) 
    self.conn.commit()
    
  def insert_into_table(self):
    sql_params = ",".join(self.fts_fields.values())
    #print("record keys")
    #printer.pprint(self.record.keys())
    #print("\nvalues only")
    #printer.pprint(self.record.values())
    sql_insert_values = [ ",".join(flatten(value)) for value in list(self.record.values())]
    #print("INSERT INTO zettels VALUES (%s)" % sql_params)
    #print(self.record.keys())
    #printer.pprint(sql_insert_values)
    self.cursor.execute("INSERT INTO zettels VALUES (%s)" % sql_params, sql_insert_values)
    self.conn.commit()

  # A term_list is a list of 3-tuples (not-option, fieldname, word

  def fts_search(self, term_list):
    safe_term_list = []
    for term in term_list:
       if type(term) == type(()) and len(term) == 3:
          (name, not_operator, words) = term
          words = unquote(words)
          if not_operator not in '-':
             not_operator = ''
          if name not in self.fts_field_names:
             continue
          for word in words.split():
             safe_term_list.append((name, ":", not_operator, word))

    #print(safe_term_list)
    fts_terms = " ".join(["".join(list(term)) for term in safe_term_list])
    Q="SELECT * from zettels where zettels match '%s'" % fts_terms
    #print(Q)
    for row in self.cursor.execute(Q):
       yield(row)
    
  def done(self):
    self.conn.commit()
    self.conn.close()
    

ZDB = 'zettels.db'

def get():
  return SQLiteFTS(ZDB, 'zettels', ZETTEL_FIELDS)

def delete():
  os.unlink(ZDB)

