#
# Author: Kevin T. Ryan (same as left, separated with dots AT gmail.com)
# Date: 2008-Feb-19 @ 12:19:24 AM

# I first checked out (which are all very good - I suggest you check them out
# as they might suit your needs better):

#   - http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/528939
#   - http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/163605
#   - http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/81252
#   - http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/52293

# While each provided the dictionary type interface that I was looking for,
# they were not quite as light-weight as I wanted (although dtuple might be -
# I didn't fetch the source for that one), or they didn't have the terribly
# simple interface that I wanted (ie, row.field_name or row['field_name'] or
# row[0] - whatever I preferred at the moment).  Although the
# "light-weightedness" of my approach might be questionable as I do a
# "fetchall" when no results are passed in - which sort of defeats the purpose
# a -little- bit.  I digress.  As such, I came up with the attached.  The
# recipe below only stores one copy of the fields which is initialized on
# __init__.  It does this in the same fashion that recipe 52293 does.  It also
# wraps each result row sort of like recipe 163605, but instead of storing a
# dictionary of the fields for every row it allows the "row" class to delegate
# back to the parent (ie, results class) by using __getattr__ judiciously.

# It also acts as an iterator for your results by defining __iter__() and
# next() methods.

# Usage:

#   conn = <connect method>
#   curs = conn.cursor()
#   curs.execute("<your SQL statement here")
#   for row in results(curs): # note, fetches all the rows 1st
#       print row.field_name
#       - OR -
#       print row['field_name']
#       - OR -
#       print row[0]
#       - OR -
#       print row[:3]

# Note that all of the above access methods are possible thanks to the pure
# goodness of Python :)  Also, you could easily improve how the data is
# fetched if you are building large queries - just delegate in each next()
# call if you need to fetch more records instead of fetching everything at the
# beginning of the call.  Finally, you could also make each row look more like
# a dictionary if you wanted to - add "has_key" method (k in
# self.parents.columns), "keys" method (self.parents.columns.keys()), etc.

class row(object):
    def __init__(self, parent, current_row):
        self.parent = parent
        self.current_row = current_row
    def __getattr__(self, name):
        try:
            return self.parent.get_item(self.current_row, name)
        except:
            raise AttributeError, "That field doesn't appear to be in the results row"
    def __getitem__(self, key):
        return self.__getattr__(key)

class results(object):
    def __init__(self, curs, results=None):
        if results is None:
            results = curs.fetchall() # too inefficient?
        self.rows = results
        # Start row at -1 so that when iteration commences (probably the only way this
        # should be called), it will update the row to point to the beginning of the results.
        self.row = row(self, -1)
        self.columns = dict( [(d[0],pos) for pos,d in enumerate(curs.description)] )
    def get_item(self, row, column):
        if column in self.columns:
            return self.rows[row][self.columns[column]]
        else:
            return self.rows[row][column] # Assumed to be a numeric reference or a slice
    def __iter__(self):
        return self
    def next(self):
        self.row.current_row += 1
        if self.row.current_row >= len(self.rows):
            raise StopIteration
        return self.row
    def __len__(self):
        return len(self.rows)
