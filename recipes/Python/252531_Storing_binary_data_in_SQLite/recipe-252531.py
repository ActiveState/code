import os
import sqlite

class Blob:
    """Automatically encode a binary string."""
    def __init__(self, s):
        self.s = s

    def _quote(self):
        return "'%s'" % sqlite.encode(self.s)

db = sqlite.connect("test.db")
cursor = db.cursor()
cursor.execute("CREATE TABLE t (b BLOB);")
s = "\0"*50 + "'"*50
cursor.execute("INSERT INTO t VALUES(%s);", Blob(s))
cursor.execute("SELECT b FROM t;")
b = cursor.fetchone()[0]
assert b == s # b is automatically decoded
db.close()
os.remove("test.db")
