#!/usr/bin/env python

class P(object):
    def __init__(self, pkg, requires):
        self.requires = requires
        self.pkg      = pkg
        self.Required = 0

    def __str__(self):
        return self.pkg

    def __repr__(self):
        return self.__str__()

    def Require(self, pkg):
        if str(pkg) in self.requires:
            return True
        return False


objs = []
# The proper dependancy order is:
# e f b g d c a
objs.append(P('a', ['b', 'c', 'd']))
objs.append(P('b', ['f']))
objs.append(P('c', ['d', 'e']))
objs.append(P('d', ['g']))
objs.append(P('e', []))
objs.append(P('f', ['e']))
objs.append(P('g', []))

print(objs)
changes = True
iters   = 0
while changes:
    changes = False
    if iters >= 5000:
        print('Poor man\'s circular dependancy detection triggered!')
        break
    else:
        iters += 1
    for a in range(0, len(objs)):
        for b in range(0, len(objs)):
            if objs[b].Require(objs[a]):
                if b < a:
                    objs.insert(a, objs.pop(b))
                    changes = True
                    break
        if changes:
            break
    if not changes:
        break
print(objs)
