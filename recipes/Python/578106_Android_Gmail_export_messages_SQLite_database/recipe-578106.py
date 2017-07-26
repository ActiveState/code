import sqlite3
import zlib

good_chars=',.0123456789@ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz~ '

conn = sqlite3.connect('gmail.db')
cursor = conn.cursor()
cursor.execute("select _id, fromAddress, subject, bodyCompressed from messages")
rows = cursor.fetchall()

for row in rows:
    fname = (str(row[0]) + row[1] + row[2])[:48]
    fname = ''.join([c for c in fname if c in good_chars])
    print fname
    with open(fname + '.html', 'wb') as fout:
        if row[3]:
            data = zlib.decompress(row[3])
            fout.write('<html><body>' + data + '</body></html>')

cursor.close()
conn.close()
