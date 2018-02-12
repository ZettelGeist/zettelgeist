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


def write_to_file(filepath, text, **kwargs):
    mode = kwargs.get("mode", "a")
    newlines = kwargs.get("newlines", 1)
    with open(filepath, mode) as outfile:
        outfile.write(text)
        if newlines:
            outfile.write("\n" * int(newlines))


def write_data(filename, mode, comment, statement):
    if not filename:
        return
    with open(filename, mode) as outfile:
        outfile.write("\n".join([comment, statement]) + "\n\n")


def dirname(path):
    return os.path.split(path)[0]


def basename(path):
    return os.path.split(path)[1]
