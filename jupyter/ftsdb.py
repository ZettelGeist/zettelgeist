# 
# ZettelGeist uses a FTS system for organizing Zettels. The index is intended
# to be emphemeral and can be regenerated at any time. The schema itself is
# ephemeral and can be augmented with additional fields of interest.
# 

import sqlite3

# This is for showing data structures only.

import pprint
printer = pprint.PrettyPrinter(indent=2)

def flatten(item):
    if type(item) != type([]):
        return [str(item)]
    if item == []:
        return item
    if isinstance(item[0], list):
        return flatten(item[0]) + flatten(item[1:])
    return item[:1] + flatten(item[1:])

class SQLiteFTS(object):  
  def __init__(self, db_name, table_name, field_names):
    self.db_name = db_name
    self.conn = sqlite3.connect(db_name)
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
           self.record[k] = doc[k]
        else:
           print("Unknown fts field %s" % k)
    self.record.update(doc)
    
  def drop_table(self):
    self.conn.execute("DROP TABLE IF EXISTS %s" % self.table_name)

  def create_table(self):
    sql_fields = ",".join(self.fts_default_record.keys())
    #print("CREATE VIRTUAL TABLE zettels USING fts4(%s)" % sql_fields)
    self.conn.execute("CREATE VIRTUAL TABLE zettels USING fts4(%s)" % sql_fields) 
    
  def insert_into_table(self):
    sql_params = ",".join(self.fts_fields.values())
    #printer.pprint(self.record)
    #printer.pprint(self.record.values())
    sql_insert_values = [ ",".join(flatten(value)) for value in list(self.record.values())]
    #print("INSERT INTO zettels VALUES (%s)" % sql_params)
    #print(self.record.keys())
    #printer.pprint(sql_insert_values)
    self.conn.execute("INSERT INTO zettels VALUES (%s)" % sql_params, sql_insert_values)

  def done(self):
    self.conn.commit()
    self.conn.close()
    

