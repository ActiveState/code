class RowObject(dict):
    """ allows access to dict via attributes as keys """

    def __init__(self, *l, **kw):
        dict.__init__(self, *l, **kw)

    def __setattr__(self, k, v):
        dict.__setitem__(self, k, v)

    def __getattr__(self, k):
        return self.get(k)


class Table(object):
    """ represents table and set operations on tables """

    def __init__(self, rows=[]):
        self.rows = rows[:]

    def append(self, obj):
        self.rows.append(obj)

    def __iter__(self):
        return iter(self.rows)

    def __getattr__(self, column):
        """ constructs intermediate table when accessing t.column """
        return ITable(self.rows, column)

    def __and__(self, other):
        """ computes intersection of two tables """
        tmp = [ r for r in self.rows if r in other.rows ]
        return Table(tmp)

    def __or__(self, other):
        """ computes union of two tables """
        tmp = self.rows[:]
        tmp.extend(other.rows[:]) # use copys of lists !
        return Table(tmp)

    def __str__(self):
        """ quite stupid, just for demonstration purposes """
        txt = "\t".join(self.rows[0].keys()).expandtabs()
        txt += "\n"
        txt += "-"*len(txt)
        for r in self.rows:
            txt += "\n"
            txt += "\t".join([str(v) for v in r.values()])
        return txt



class ITable(object):
    """ intermediate table for storing fixed column name internally """

    def __init__(self, rows, column):
        self.rows=rows[:]
        self.column=column

    def _extract(self, fun):
        return Table([ row for row in self.rows if fun(row.get(self.column)) ]) 

    def __le__(self, limit):
        return self._extract(lambda v: v<=limit)

    def __ge__(self, limit):
        return self._extract(lambda v: v>=limit)

    def __eq__(self, other):
        return self._extract(lambda v: v==other)


# store original max function for later usage
__savedMax = max

def max(*what):
    """ computes max of a given column if argument is of type ITable
        and regular max elsewise.  """

    if isinstance(what[0], ITable): 
        it = what[0]
        return __savedMax([row.get(it.column) for row in it.rows])
    return __savedMax(what)

if __name__ == "__main__":

    t=Table()
    t.append(RowObject(a=1, b=1))
    t.append(RowObject(a=2, b=2))
    t.append(RowObject(a=3, b=1))
    t.append(RowObject(a=4, b=2))

    print 
    print ">>> Table:"
    print t
    print

    print ">>> max of column b:"
    print max(t.b)
    print

    print ">>> rows with maximal b value:"
    print t.b == max(t.b)
    print

    print ">>> rows with a>=2 and a<=3:"
    print (t.a>=2) & (t.a <=3)
    print

    print ">>> rows with a==1 or b==2:"
    print (t.a==1) | (t.b ==2)
