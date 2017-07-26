import exceptions
import sys
import types

def copyright():
    print("""Copyright 2001 by Peter Olsen, P.E., p@sigmaxi.org
            May be used for any purpose without payment of royalty
            provided this copyright is retained.
            
            This code is provided in the hope that it may be useful
            but with WITH ABSOLUTELY NO WARRANTY WHATSOEVER,
            including any warranty of merchantability or fitness for any
            particular purpose.

            If this code works, fine; if it doesn't, I'm not responsible.""") 
          
class RaggedArray2D(dictionary):

    """This class implements 2-dimensional ragged arrays as nested Dictionaries.

    Keys are 2-tuples, conceptually "rows" and "columns."

    Each "row" is a subdictionary returned by the first key in a
    keyTuple.  Each "column" is a subdictionary built by extracting
    appropriate elements from each row.  So, for faster code, try to
    access first by row, then by column rather than the other way around

    This class is implemented as two layers of nested dictionaries instead of
    as a single dictionary keyed by the tuples directly because I'm writing it
    for an application in which I want to operate entire rows.  This  approach
    makes it much easier.

    Note: This implementation subclasses a built-in data type, and so requires 
    Python 2.2 or later.  This meets my requirements, but it may not meet
    yours. 
 
    Klaus Alexander Seistrup has described a way to get around this 
    restriction by substituting UserDict.UserDict for dictionary as 
    the base class.  I believe this solves the problem for versions at least
    as far back as 1.5.2.  This approach will require some editing of
    the insertion and retrieval functions to make it work.  

    Thanks Klaus!"""

    def insert(self, keyTuple, newThing):
        """Stores newThing in place specified by keyTuple, returns oldThing.

        keyTuple is a 2-tuple of coordinates.
        thing is any object that can be stored in a dictionary.

        Returns None if there was no old thing at key."""

        if not self.checkKeyTuple(keyTuple):
            raise RaggedArrayException, "Bad keyTuple."
        else:
            # Key was a tuple of length 2
            # So, extract two keys.
            key1 = keyTuple[0]
            key2 = keyTuple[1]

            # So, now we have a sub-dictionary in the right position of
            # raggedArray.  Let's save the oldThing and insert the newThing.
            row = self.getRow(key1)
            oldThing = row.get(key2, None)
            row[key2] = newThing
        # We've saved the oldThing and inserted the newThing.  We're done!
        return oldThing

    def retrieve(self, keyTuple):
        """Retrieves oldThing from place specified by keyTuple.

        keyTuple is a 2-tuple of coordinates."""

        # FIXME: can retrieve() share more code with insert()?
        if not self.checkKeyTuple(keyTuple):
            raise RaggedArrayException, "Bad keyTuple."
        else:
            # Key was a tuple of length 2
            # So, extract two keys.
            key1 = keyTuple[0]
            key2 = keyTuple[1]

            # So, now we have a sub-dictionary in the right position of
            # raggedArray.
            row = self.getRow(key1)
            oldThing = row.get(key2, None)
        return oldThing

    def checkKeyTuple(self, keyTuple):
        """Checks keyTuple validity. Returns boolean."""
        
        # Is the key a tuple?  If not, it's an error.
        if not isinstance(keyTuple, types.TupleType):
            result = 0
            raise RaggedArrayException, "checkKeyTuple: keyTuple not a tuple."
        # Does the keyTuple have two keys?  If not, it's an error.
        elif len(keyTuple) != 2:
            result = 0
            raise RaggedArrayException, "checkKeyTuple: keyTuple wrong length."
        else:
            result = 1
        return result

    def getRow(self, key):
        """Gets or creates the row subdirectory matching key.

        Note that the "rows" returned by this method need not be complete.
        They will contain only the items corresponding to the keys that
        have actually been inserted.  Other items will not be present,
        in particular they will not be represented by None."""
        
        # Get whatever is located at the first key
        thing = self.get(key, None)

        # If thing is a dictionary, return it.
        if isinstance(thing, dictionary):
            row = thing

        # If thing is None, create a new dictionary and return that.
        elif isinstance(thing, types.NoneType):
            row = {}
            self[key] = row

        # If thing is neither a dictionary nor None, then it's an error.
        else:
            row = None
            raise RaggedArrayException, "getRow: thing was not a dictionary."
        return row  

    def getColumn(self, columnKey):
        """Gets or creates the column subdirectory matching key.

        Note that the "columns" returned by this method need not be complete.
        They will contain only the items corresponding to the keys that
        have actually been inserted.  Other items will not be present,
        in particular they will not be represented by None."""
        
        # Get a list of the keys to the primary dictionary
        rows = self.keys()

        # Create the empty column dictionary
        column = {}

        # Now index through the rows, retrieving the appropriate "column"
        # entries and adding them to the column
        for row in rows:
            thisRow = self.getRow(row)
            if thisRow.has_key(columnKey):
                column[row] = thisRow[columnKey]
        return column
    
class RaggedArrayException(exceptions.Exception):
    def __init__(self, args=None):
        self.args = "RaggedArray: " + args
        

       
