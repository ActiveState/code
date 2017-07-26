import types

# Andrew Konstantaras
# konsta@speakeasy.org
# 12 May 2008
# Feel free to use with attribution where appropriate.  If you find any errors or make any improvements, please make those freely available
# (again, where appropriate).
#
# These functions are designed to make SQL insert statements from user defined objects.  An object is passed to the main
# function makeObjInsertStrings along with a tuple of the valid object names and the function will return a 3 value tuple.
# If the object is not an instance of the types listed in the passed tuple of valid object names, the 3 value tuple returned is None, None, None
# If a valid object is returned, the returned tuple contains:
#
# strCols            a string of the the attribute names of the object that are of type Boolean, Int, Long,
#                    Float, StringType, StringTypes, None
# strVals            a string of the corresponding values of the above object separated by commas (each string
#                    surrounded with dblquotes, numbers are not)
# lstExcludedAttrib  a list of attributes that were excluded from the list because they were not of a valid type
#
# Current expects a tuple containing all the valid objects.
#
# If the default blnUseParens is set to False, the strCols and strVals will not be surrounded with parens, otherwise
# parens will be included
#
# ***To be implemented****
# I'd like to create code that will identify all the user defined objects that exist at the time this function is called, but
#I kept running into a snags, so I made the list passed parameter with a default of none to allow for the code to be added nicely.
#
# If the default blnGetAllAttrib is set to False, then only valid attributes with values (i.e., empty strings and None not included)
#will appear in the strCols and strVals


def makeObjInsertStrings( obj, tplObjects = None, blnUseParens=True, blnGetAllAttrib=True ):
    # Returns a 3 val tuple, the first two of which are strings which can be dropped into a MySQL Insert statement for (1) column names and (2) values
    
    if not tplObjects:
        return None, None, None
    if isinstance( obj, tplObjects ):    #find out what got passed - valid objects must be included in tuple tplObjects
        strDblQuote = '"'
        lstCols = list()
        lstVals = list()
        lstExcludedAttrib = list()
        dctObj = vars( obj )
        lstObjVarNames = dctObj.keys()
        if blnGetAllAttrib:
            tplValidTypes = ( types.BooleanType, types.FloatType, types.IntType, types.LongType, types.StringType, types.StringTypes, types.NoneType )
            for varName in lstObjVarNames:
                val = dctObj[ varName ]
                if isinstance( val, tplValidTypes ):
                    lstCols.append( varName )
                    if val or val == 0:
                        lstVals.append( dctObj[ varName ] )
                    else:
                        lstVals.append('')
                else:
                    lstExcludedAttrib.append( varName )
        if blnUseParens:
            strCols = joinListItems( lstCols )
            strVals = joinListItems( lstVals )
        else:
            strCols = joinListItems( lstCols, blnUseParens=False )
            strCols = joinListItems( lstVals, blnUseParens=False )
        strCols = strCols.replace('"', '')
        return strCols, strVals, lstExcludedAttrib
    else:
        print 'No object passed.'
        return None, None, None


def getValueStrings( val, blnUgly=True ):
    #Used by joinWithComma function to join list items for SQL queries.
    #Expects to receive 'valid' types, as this was designed specifically for joining object attributes and nonvalid attributes were pulled.
    #If the default blnUgly is set to false, then the nonvalid types are ignored and the output will be pretty, but the SQL Insert statement will
    #probably be wrong.
    tplStrings = (types.StringType, types.StringTypes )
    tplNums = ( types.FloatType, types.IntType, types.LongType, types.BooleanType )
    if isinstance( val, tplNums ):
        return '#num#'+ str( val ) + '#num#'
    elif isinstance( val, tplStrings ):
        strDblQuote = '"'
        return strDblQuote + val + strDblQuote
    else:
        if blnUgly == True:
            return "Error: nonconvertable value passed - value type: %s" % type(val )
        else:
            return None

def joinListItems( lstStart, strDelim = ',', strNumDelim='#num#', blnUseParens = True ):
    #Replicates the join function associated with arrays in other languages, allowing for strings and numbers to be joined without converting the nums to strings
    #Created specifically for SQL Insert Statement generation.  Currently only allows for items to be separated by a comma.
    #
    # ***To be implemented:
    # Allow for additional delimiters to join the list items.  
    if strDelim == ',':
        strResult = reduce( joinWithComma, lstStart )
        strResult = strResult.replace(strNumDelim+'"', '')
        strResult = strResult.replace(strNumDelim, '')
        strResult = '(' + strResult + ')'
        strResult = strResult.replace('", ")', '", "")')
        strResult = strResult.replace(', ",', ', "",')
        strResult = strResult.replace('"", ",', '"", "",')
        if strResult[0:3] == '(",':
            strResult = '("",' + strResult[3:]
        if not blnUseParens:
            strResult = strResult[1:len(strResult)-1]
    return strResult 
    
def joinWithComma( x, y ):
    strX = getValueStrings( x )
    strY = getValueStrings( y )
    if strX:
        if strY:
            strResult = strX + ', ' + strY
            strResult = strResult.replace('""', '"')
        else:
            strResult = x
    else:
        if strY:
            strResult = y
        else:
            strResult = ""
    return strResult


####Main with simple test

if __name__ == '__main__':
    class simple():
        def __init__(self):
            self.Name = ""
            self.Codes = list()
            self.NumCodes = 0
            self.EntryType = None
            self.OtherValue = 0
            self.Comment = None
    t = simple()
    t.Name = "MyName"
    t.Comment = ""
    t.NumCodes = 1
    t.OtherValue = 0
    tplObjects = ( simple )                         #I've only defined one class, so that's all I'm passing to the makeObjInsertStrings function
    strCols, strVals, lstExcluded = makeObjInsertStrings( t, tplObjects )
    print 'Columns: %s\nValues: %s' % (strCols, strVals )
    print 'List of Attributes ignored:'
    for attr in lstExcluded:
        print "   Name of attribute in t: ", attr, ' - which is of type ', type( eval("t."+attr) )
    
    
