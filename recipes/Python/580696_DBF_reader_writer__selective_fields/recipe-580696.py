import struct, datetime, decimal, itertools
from collections import namedtuple

FI = namedtuple('FieldInfo', ('name', 'typ', 'size', 'deci',
                              'fmt', 'fmtsiz', 'keep', 'seekme'))

def dbfreader(f, names, nullreplace=None):
    """Returns an iterator over records in a Xbase DBF file.

    The first row returned contains the field names. The second row
    contains field specs: (type, size, decimal places). Subsequent rows
    contain the data records. If a record is marked as deleted, it is
    skipped.

    names is the field names to extract. The value of nullreplace is
    used with data of type 'N' as a replacement for '\0'.

    File should be opened for binary reads.

    """
    # See DBF format spec at:
    # http://www.pgts.com.au/download/public/xbase.htm#DBF_STRUCT

    numrec, lenheader = struct.unpack('<xxxxLH22x', f.read(32))
    numfields = (lenheader - 33) // 32

    fields = [FI('DeletionFlag', 'C', 1, 0,
                 '1s', struct.calcsize('1s'), True, 0)] # discarded in main loop

    for fieldno in xrange(numfields):
        name, typ, size, deci = struct.unpack('<11sc4xBB14x', f.read(32))
        name = name.replace('\0', '')       # eliminate NULs from string
        fmt = str(size) + 's'
        prev = fields[fieldno]
        fi = FI(name, typ, size, deci, fmt, struct.calcsize(fmt), name in names,
                prev.seekme + prev.size)
        fields.append(fi)

    selfields = [field for field in fields if field.keep]
    yield [field.name for field in selfields[1:]]
    yield [tuple(field[1:4]) for field in selfields[1:]]

    terminator = f.read(1)
    assert terminator == '\r'

    for i in xrange(numrec):
        refaddr = f.tell()
        record = []
        for field in selfields:
            f.seek(refaddr + field.seekme)
            record.append(struct.unpack(field.fmt, f.read(field.fmtsiz))[0])

        if record[0] != ' ':
            continue                        # deleted record
        result = []
        for sf, value in itertools.izip(selfields, record):
            if sf.name == 'DeletionFlag':
                continue
            if sf.typ == "N":
                value = value.replace('\0', '').lstrip()
                if value == '':
                    value = nullreplace
                elif sf.deci:
                    value = decimal.Decimal(value)
                else:
                    value = int(value)
            elif sf.typ == 'D':
                y, m, d = int(value[:4]), int(value[4:6]), int(value[6:8])
                value = datetime.date(y, m, d)
            elif sf.typ == 'L':
                value = (value in 'YyTt' and 'T') or (value in 'NnFf' and 'F') or '?'
            elif sf.typ == 'F':
                value = float(value)
            result.append(value)
        f.seek(refaddr + fields[-1].seekme + fields[-1].fmtsiz)
        yield result

def dbfwriter(f, fieldnames, fieldspecs, records, nullreplace=None):
    """Return a string suitable for writing directly to a binary dbf file.

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

    The value of nullreplace is compared with values of type N and, if
    equal, replaced with '\0' in the output.

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
                if value != nullreplace:
                    value = str(value).rjust(size, ' ')
                else:
                    value = '\0'.rjust(size, ' ')
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
