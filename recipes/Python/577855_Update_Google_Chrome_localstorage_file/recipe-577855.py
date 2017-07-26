import sqlite3, StringIO, sys

def buf2unicode(data):
    u = StringIO.StringIO()
    for i in xrange(0, len(data), 2):
        f = unichr(ord(data[i+1]) << 8 | ord(data[i+0]))
        u.write(f)
    return u.getvalue()

def unicode2buf(data):
    assert(type(data) == unicode)
    ba = bytearray()
    for i in data:
        t = ord(i)
        b1 = 255 & (t >> 8)
        b0 = 255 & t
        ba.append(b0)
        ba.append(b1)
    return buffer(ba)

def main(name):
    try:
        conn = sqlite3.connect(name)
    except:
        print name, "can't be opened."

    c = conn.cursor()
    try:
        r = c.execute('select * from ItemTable')
    except:
        print name, "is not a localstorage file."

    data = {}
    for key, val in r:
        if type(val) == unicode:
            data[key] = unicode2buf(val)

    for k in data:
        c.execute('update ItemTable set value=? where key=?', (data[k], k))
        print "Updated", k

    conn.commit()
    c.close()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print "Usage: %s target_filename" % sys.argv[0]
        print "target file will be modified. Please make backups."
