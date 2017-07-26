import re
from struct import unpack, pack
    
def parse(buf):
    # Compile a regex that can parse a buffer with an arbitrary number of
    # records, each consisting of a short, a null-terminated string, 
    # and two more shorts.  Incomplete records at the end of the file 
    # will be ignored.  re.DOTALL ensures we treat newlines as data.
    r = re.compile("(..)(.*?)\0(..)(..)", re.DOTALL)

    # packed will be a list of tuples: (packed short, string, short, short).
    # You can use finditer instead to save memory on a large file, but
    # it will return MatchObjects rather than tuples.
    packed = r.findall(buf)

    # Create an unpacked list of tuples, mirroring the packed list.
    # Perl equivalent: @objlist = unpack("(S Z* S S)*", $buf);
    # Note that we do not need to unpack the string, because its 
    # packed and unpacked representations are identical.
    objlist = map(lambda x: (short(x[0]), x[1], short(x[2]), short(x[3])), packed)

    # Alternatively, unpack using a list comprehension:
    # objlist = [ ( short(x[0]), x[1], short(x[2]), short(x[3]) ) for x in packed ]
        
    # Create a dictionary from the packed list.  The records hold object id,
    # description, and x and y coordinates, and we want to index by id.
    # We could also create it from the unpacked list, of course.
    objdict = {}
    for x in packed:
        id = short(x[0])
        objdict[id] = {}
        objdict[id]["desc"] = x[1]
        objdict[id]["x"] = short(x[2])
        objdict[id]["y"] = short(x[3])

    return objlist, objdict

# Converts 2-byte string to little-endian short value.
# unpack returns a tuple, so we grab the first (and only) element.
def short(x):
    return unpack("<H", x)[0]

# Packs the arguments into a string that parse() can read,
# for testing.
def packobj(id, desc, x, y):
    return pack("<H", id) + desc + "\0" + pack("<HH", x, y)


if __name__ == '__main__':

    # Pack test objects into string buffer.  Normally, you'd load buf
    # with file data, perhaps with buf = file(filename, "rb").read()
    buf = ""
    buf += packobj(768, "golden helmet", 3, 4)
    buf += packobj(234, "windmill", 20, 30)
    # Test inclusion of newline in string
    buf += packobj( 35, "pitcher\nand stone", 1, 2)
    # Also add a bit of garbage at the end,
    # which the parser should ignore.
    buf += "garbage";

    # Parse buffer into list and dictionary of objects
    olist, odict = parse(buf)
    print olist
    print odict
    print odict[35]["desc"]  # should retain the newline
