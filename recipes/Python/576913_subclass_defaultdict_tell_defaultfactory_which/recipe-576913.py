from collections import defaultdict
from itertools import count


class Var(object):

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "Var(%s)" % self.name


class vardict(defaultdict):

    def __init__(self, *args, **kwargs):
        super(vardict, self).__init__(Var, *args, **kwargs)

    def __missing__(self, key, unique=count()):
        if self.default_factory is None:
            raise KeyError(key)
        if key == "_":
            return self.default_factory(key + str(next(unique)))
        self[key] = value = self.default_factory(key)
        return value


if __name__ == "__main__":

    vdict = vardict()
    vlist = []

    vlist.append(vdict["First"])
    vlist.append(vdict["Second"])
    vlist.append(vdict["_"])
    vlist.append(vdict["First"])
    vlist.append(vdict["Second"])
    vlist.append(vdict["_"])

    vlist.sort()

    print
    for key, value in vdict.items():
        print key, ":", value

    print
    for each in vlist:
        print id(each), ":", each
