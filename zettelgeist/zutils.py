import argparse
import os
import os.path
import sqlite3

from . import zettel

# Compute MD5 for large files
#
# Credit to:
# stackoverflow.com/questions/1131220/get-md5-hash-of-big-files-in-python

def md5_for_file(f, block_size=2**20):
    md5 = hashlib.md5()
    while True:
        data = f.read(block_size)
        if not data:
            break
        md5.update(data)
    return md5.digest()
