import struct, datetime, decimal, itertools

def dbfreader(f):
    """Returns an iterator over records in a Xbase DBF file.

    The first row returned contains the field names.
    The second row contains field specs: (type, size, decimal places).
    Subsequent rows contain the data records.
    If a record is marked as deleted, it is skipped.

    File should be opened for binary reads.

    """
    # See DBF format spec at:
    #     http://www.pgts.com.au/download/public/xbase.htm#DBF_STRUCT

    numrec, lenheader = struct.unpack('<xxxxLH22x', f.read(32))    
    numfields = (lenheader - 33) // 32

    fields = []
    for fieldno in xrange(numfields):
        name, typ, size, deci = struct.unpack('<11sc4xBB14x', f.read(32))
        name = name.replace('\0', '')       # eliminate NULs from string   
        fields.append((name, typ, size, deci))
    yield [field[0] for field in fields]
    yield [tuple(field[1:]) for field in fields]

    terminator = f.read(1)
    assert terminator == '\r'

    fields.insert(0, ('DeletionFlag', 'C', 1, 0))
    fmt = ''.join(['%ds' % fieldinfo[2] for fieldinfo in fields])
    fmtsiz = struct.calcsize(fmt)
    for i in xrange(numrec):
        record = struct.unpack(fmt, f.read(fmtsiz))
        if record[0] != ' ':
            continue                        # deleted record
        result = []
        for (name, typ, size, deci), value in itertools.izip(fields, record):
            if name == 'DeletionFlag':
                continue
            if typ == "N":
                value = value.replace('\0', '').lstrip()
                if value == '':
                    value = 0
                elif deci:
                    value = decimal.Decimal(value)
                else:
                    value = int(value)
            elif typ == 'D':
                y, m, d = int(value[:4]), int(value[4:6]), int(value[6:8])
                value = datetime.date(y, m, d)
            elif typ == 'L':
                value = (value in 'YyTt' and 'T') or (value in 'NnFf' and 'F') or '?'
            elif typ == 'F':
                value = float(value)
            result.append(value)
        yield result


def dbfwriter(f, fieldnames, fieldspecs, records):
    """ Return a string suitable for writing directly to a binary dbf file.

    File f should be open for writing in a binary mode.

    Fieldnames should be no longer than ten characters and not include \x00.
    Fieldspecs are in the form (type, size, deci) where
        type is one of:
            C for ascii character data
            M for ascii character memo data (real memo fields not supported)
            D for datetime objects
            N for ints or decimal objects
            L for logical values 'T', 'F', or '?'
        size is the field width
        deci is the number of decimal places in the provided decimal object
    Records can be an iterable over the records (sequences of field values).
    
    """
    # header info
    ver = 3
    now = datetime.datetime.now()
    yr, mon, day = now.year-1900, now.month, now.day
    numrec = len(records)
    numfields = len(fieldspecs)
    lenheader = numfields * 32 + 33
    lenrecord = sum(field[1] for field in fieldspecs) + 1
    hdr = struct.pack('<BBBBLHH20x', ver, yr, mon, day, numrec, lenheader, lenrecord)
    f.write(hdr)
                      
    # field specs
    for name, (typ, size, deci) in itertools.izip(fieldnames, fieldspecs):
        name = name.ljust(11, '\x00')
        fld = struct.pack('<11sc4xBB14x', name, typ, size, deci)
        f.write(fld)

    # terminator
    f.write('\r')

    # records
    for record in records:
        f.write(' ')                        # deletion flag
        for (typ, size, deci), value in itertools.izip(fieldspecs, record):
            if typ == "N":
                value = str(value).rjust(size, ' ')
            elif typ == 'D':
                value = value.strftime('%Y%m%d')
            elif typ == 'L':
                value = str(value)[0].upper()
            else:
                value = str(value)[:size].ljust(size, ' ')
            assert len(value) == size
            f.write(value)

    # End of file
    f.write('\x1A')


# -------------------------------------------------------
# Example calls
if __name__ == '__main__':
    import sys, csv
    from cStringIO import StringIO
    from operator import itemgetter

    # Read a database
    filename = '/pydev/databases/orders.dbf'      
    if len(sys.argv) == 2:
        filename = sys.argv[1]
    f = open(filename, 'rb')
    db = list(dbfreader(f))
    f.close()
    for record in db:
        print record
    fieldnames, fieldspecs, records = db[0], db[1], db[2:]

    # Alter the database
    del records[4]
    records.sort(key=itemgetter(4))

    # Remove a field
    del fieldnames[0]
    del fieldspecs[0]
    records = [rec[1:] for rec in records]

    # Create a new DBF
    f = StringIO()
    dbfwriter(f, fieldnames, fieldspecs, records)

    # Read the data back from the new DBF
    print '-' * 20    
    f.seek(0)
    for line in dbfreader(f):
        print line
    f.close()

    # Convert to CSV
    print '.' * 20    
    f = StringIO()
    csv.writer(f).writerow(fieldnames)    
    csv.writer(f).writerows(records)
    print f.getvalue()
    f.close()




# Example Output
"""
['ORDER_ID', 'CUSTMR_ID', 'EMPLOY_ID', 'ORDER_DATE', 'ORDER_AMT']
[('C', 10, 0), ('C', 11, 0), ('C', 11, 0), ('D', 8, 0), ('N', 12, 2)]
['10005     ', 'WALNG      ', '555        ', datetime.date(1995, 5, 22), Decimal("173.40")]
['10004     ', 'BMARK      ', '777        ', datetime.date(1995, 5, 18), Decimal("3194.20")]
['10029     ', 'SAWYH      ', '777        ', datetime.date(1995, 6, 29), Decimal("97.30")]
['10013     ', 'RITEB      ', '777        ', datetime.date(1995, 6, 2), Decimal("560.40")]
['10024     ', 'RATTC      ', '444        ', datetime.date(1995, 6, 21), Decimal("2223.50")]
['10018     ', 'RATTC      ', '444        ', datetime.date(1995, 6, 12), Decimal("1076.05")]
['10025     ', 'RATTC      ', '444        ', datetime.date(1995, 6, 23), Decimal("185.80")]
['10038     ', 'OLDWO      ', '111        ', datetime.date(1995, 7, 14), Decimal("863.96")]
['10002     ', 'MTIME      ', '333        ', datetime.date(1995, 5, 16), Decimal("731.80")]
['10007     ', 'MORNS      ', '444        ', datetime.date(1995, 5, 24), Decimal("1405.00")]
['10026     ', 'MORNS      ', '555        ', datetime.date(1995, 6, 26), Decimal("17.40")]
['10030     ', 'LILLO      ', '111        ', datetime.date(1995, 7, 3), Decimal("909.91")]
['10022     ', 'LAPLA      ', '111        ', datetime.date(1995, 6, 19), Decimal("671.50")]
['10035     ', 'HIGHG      ', '111        ', datetime.date(1995, 7, 11), Decimal("1984.83")]
['10033     ', 'FOODG      ', '333        ', datetime.date(1995, 7, 6), Decimal("3401.32")]
--------------------
['CUSTMR_ID', 'EMPLOY_ID', 'ORDER_DATE', 'ORDER_AMT']
[('C', 11, 0), ('C', 11, 0), ('D', 8, 0), ('N', 12, 2)]
['MORNS      ', '555        ', datetime.date(1995, 6, 26), Decimal("17.40")]
['SAWYH      ', '777        ', datetime.date(1995, 6, 29), Decimal("97.30")]
['WALNG      ', '555        ', datetime.date(1995, 5, 22), Decimal("173.40")]
['RATTC      ', '444        ', datetime.date(1995, 6, 23), Decimal("185.80")]
['RITEB      ', '777        ', datetime.date(1995, 6, 2), Decimal("560.40")]
['LAPLA      ', '111        ', datetime.date(1995, 6, 19), Decimal("671.50")]
['MTIME      ', '333        ', datetime.date(1995, 5, 16), Decimal("731.80")]
['OLDWO      ', '111        ', datetime.date(1995, 7, 14), Decimal("863.96")]
['LILLO      ', '111        ', datetime.date(1995, 7, 3), Decimal("909.91")]
['RATTC      ', '444        ', datetime.date(1995, 6, 12), Decimal("1076.05")]
['MORNS      ', '444        ', datetime.date(1995, 5, 24), Decimal("1405.00")]
['HIGHG      ', '111        ', datetime.date(1995, 7, 11), Decimal("1984.83")]
['BMARK      ', '777        ', datetime.date(1995, 5, 18), Decimal("3194.20")]
['FOODG      ', '333        ', datetime.date(1995, 7, 6), Decimal("3401.32")]
....................
CUSTMR_ID,EMPLOY_ID,ORDER_DATE,ORDER_AMT
MORNS      ,555        ,1995-06-26,17.40
SAWYH      ,777        ,1995-06-29,97.30
WALNG      ,555        ,1995-05-22,173.40
RATTC      ,444        ,1995-06-23,185.80
RITEB      ,777        ,1995-06-02,560.40
LAPLA      ,111        ,1995-06-19,671.50
MTIME      ,333        ,1995-05-16,731.80
OLDWO      ,111        ,1995-07-14,863.96
LILLO      ,111        ,1995-07-03,909.91
RATTC      ,444        ,1995-06-12,1076.05
MORNS      ,444        ,1995-05-24,1405.00
HIGHG      ,111        ,1995-07-11,1984.83
BMARK      ,777        ,1995-05-18,3194.20
FOODG      ,333        ,1995-07-06,3401.32
"""
