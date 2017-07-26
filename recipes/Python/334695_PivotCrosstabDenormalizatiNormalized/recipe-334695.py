def pivot(table, left, top, value):
    """
    Creates a cross-tab or pivot table from a normalised input table. Use this
    function to 'denormalize' a table of normalized records.
    
    * The table argument can be a list of dictionaries or a Table object.
    (http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/334621)
    * The left argument is a tuple of headings which are displayed down the 
    left side of the new table.
    * The top argument is a tuple of headings which are displayed across the 
    top of the new table.
    Tuples are used so that multiple element headings and columns can be used.
    
    Eg. To transform the list (listOfDicts):
    
    Name,   Year,  Value
    -----------------------
    'Simon', 2004, 32
    'Russel', 2004, 64
    'Simon', 2005, 128
    'Russel', 2005, 32
    
    into the new list:
    
    'Name',   2004, 2005
    ------------------------
    'Simon',  32,     128
    'Russel',  64,     32
    
    you would call pivot with the arguments:
    
    newList = pivot(listOfDicts, ('Name',), ('Year',), 'Value')
    
    """
    rs = {}
    ysort = []
    xsort = []
    for row in table:
        yaxis = tuple([row[c] for c in left])
        if yaxis not in ysort: ysort.append(yaxis)
        xaxis = tuple([row[c] for c in top])
        if xaxis not in xsort: xsort.append(xaxis)
        try:
            rs[yaxis]
        except KeyError:
            rs[yaxis] = {}
        if xaxis not in rs[yaxis]:
            rs[yaxis][xaxis] = 0
        rs[yaxis][xaxis] += row[value]
            
    headings = list(left)
    headings.extend(xsort)
    
    t = []
    #If you want a list of dictionaries returned, use a cheaper alternative,
    #the Table class at:
    #       http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/334621
    #and replace the above line with this code:
    #t = Table(*headings)

    for left in ysort:
        row = list(left)
        row.extend([rs[left][x] for x in rs[left]])
        t.append(dict(zip(headings,row)))
    return t


if __name__ == "__main__":
    import random
    #Build a list of dictionaries
    c = "Employee","Year","Month","Value"
    d = []
    for y in xrange(2003,2005):
        for m in xrange(1,13):
            for e in xrange(1,6):
                d.append(dict(zip(c,(e,y,m,random.randint(10,90)))))
    #pivot the list contents using the 'Employee' field for the left column,
    #and the 'Year' field for the top heading and the 'Value' field for each
    #cell in the new table.
    t = pivot(d,["Employee"],["Year"],"Value")
    for row in t:
        print row
