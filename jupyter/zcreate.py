#
# zcreate - create the Zettel database
#

import os.path

from ftsdb import *

sql = SQLiteFTS('zettels.db', 'zettels', ['title', 'tags', 'mentions', 'outline', 'cite', 'dates', 'summary', 'text', 'bibkey', 'bibtex', 'ris', 'inline', 'note' ])


sql.drop_table()
sql.create_table()
sql.done()

if os.path.exists('zettels.db'):
  print("Zettle DB created successfully.")
else:
  print("Zettle DB was NOT created successfully. Directory writable?")

