import re

class PatternList( object ):
    """A Patternlist is a list of regular expressions. the 'in' operator
    allows a string to be compared against each expression (using search 
    NOT match)"""
    def __init__(self , patterns = []):
        self.patterns = []
        for p in patterns:
            self.add( p )        
    def add( self , pattern ):
        pat = re.compile( pattern )
        self.patterns.append( pat )
    def __contains__(self , item ):
        ret = False
        for p in self.patterns:
            if p.search( item ):
                ret= True
                break
        return ret       

if __name__=="__main__":
    examplelist = PatternList( [ ".*txt$"  ,  ".*doc$"  ])
    assert( "test.txt" in examplelist )
    assert( "test.xls" not in examplelist )
