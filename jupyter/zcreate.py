#
# zcreate - create the Zettel database
#

import os.path

from ftsdb import getDB

zdb = getDB()
zdb.drop_table()
zdb.create_table()
zdb.done()

