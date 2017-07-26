from __future__ import with_statement
from contextlib import contextmanager

@contextmanager
def pickled(filename):
    if os.path.isfile(filename):
        data = pickle.load(open(filename))
    else:
        data = {}

    def getter(item, type):
        if item in data:
            return data[item]
        else:
            data[item] = type()
            return data[item]

    yield getter

    pickle.dump(data, open(filename, "w"))

# Here is an example usage:
with pickled("foo.db") as p:
    p("users", list).append(["srid", "passwd", 23])
