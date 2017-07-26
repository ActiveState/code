#LL2XML.py
"""
See http://www.outwardlynormal.com/python/ll2XML.htm for full documentation.

This module converts a list of lists into xml
(e.g.a parsed comma separated values file or whatever).
With the proper arguments, the XML output will be an HTML table.
(See the test function for an example.)

If you want to use a csv as input, you will first need to get
hold of a csv parser to create the list of lists.
Examples include those at:
http://tratt.net/laurie/python/asv/
and
http://www.object-craft.com.au/projects/csv/
"""

# set up exceptions
class Error(Exception):
    def __init__(self, errcode,  heading_num = 0, sublist_length = 0):
        self.errcode = errcode
        if self.errcode == "Length Error - Sublists":
            self.message = ["All the sublists must be of uniform length."]
        elif self.errcode == "Heading Error - Empty Item":
            self.message = ["There is at least one empty heading item.\n",
                       "Please supply only non-empty headings."]
        elif self.errcode == "Heading Error - heading/sublist missmatch":
            self.message = ["Number of headings=",`heading_num`, "\n",
                          "Number of elements in sublists=", `sublist_length`, "\n",
                          "These numbers must be equal."]
            print self.message
        else: self.message = ""
        self.errmsg = "".join(self.message)
        
    def __str__(self):
        return (self.errmsg)
    pass

def escape(s):
    """Replace special characters '&', "'", '<', '>' and '"' by XML entities."""
    s = s.replace("&", "&amp;") # Must be done first!
    s = s.replace("'", "&apos;")
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    s = s.replace('"', "&quot;")
    return s

def cleanString(s, ident):
    if type(s) != type(""):
        s = `s`
    s = escape(s)
    if ident == "tag":
        s = s.lower()
        s = s.replace(" ", "_")
    return s

def LL2XML(LL,headings_tuple = (), root_element = "rows", row_element = "row", xml_declared = "yes"):
    if headings_tuple == "table":
        td_list = []
        for item in LL[0]:
            td_list.append("td")
        headings_tuple = tuple(td_list)
        root_element = "table"
        row_element = "tr"
        xml_declared = "no"
        
    root_element = cleanString(root_element, "tag")
    row_element = cleanString(row_element, "tag")
    if headings_tuple  == (): 
        headings = [cleanString(s,"tag") for s in LL[0]]
        LL = LL[1:]         # remove now redundant heading row
    else:
        headings = [cleanString(s,"tag") for s in headings_tuple]
        
    # Sublists all of the same length?
    if ['!' for sublist in LL if len(sublist) != len(LL[0])]:
        raise Error("Length Error - Sublists")
        
    #check headings
    heading_num = len(headings)
    if heading_num != len(LL[0]):
        raise Error("Heading Error - heading/sublist missmatch", heading_num, len(LL[0]))
    
    for item in headings:
        if not cleanString(item,"heading"):
            raise Error("Heading Error - Empty Item")
        else:
            pass
    
    # Do the conversion
    xml = ""
    if xml_declared == "yes":
        xml_declaration = '<?xml version="1.0" encoding="iso-8859-1"?>\n'
    else:
        xml_declaration = ""
    bits = []
    add_bit = bits.append
    add_bit(xml_declaration)
    add_bit('<')
    add_bit(root_element)
    add_bit('>')
    for sublist in LL:
        add_bit("\n  <")
        add_bit(row_element)
        add_bit(">\n")
        i = 0
        for item in sublist:
            tag = headings[i]
            item = cleanString(item, "item")
            add_bit("    <")
            add_bit(tag)
            add_bit(">")
            add_bit(item)
            add_bit("</")
            add_bit(tag)
            add_bit(">\n")
            i = i+1
        add_bit("  </")
        add_bit(row_element)
        add_bit(">")
    add_bit("\n</")
    add_bit(root_element)
    add_bit(">")
    xml = "".join(bits)
    return xml

def test():
    LL = [['Login', 'First Name', 'Last Name', 'Job', 'Group', 'Office', 'Permission'],
           ['auser', 'Arnold', 'Atkins', 'Partner', 'Tax', 'London', 'read'],
           ['buser', 'Bill', 'Brown', 'Partner', 'Tax', 'New York', 'read'],
           ['cuser', 'Clive', 'Cutler', 'Partner', 'Management', 'Brussels', 'read'],
           ['duser', 'Denis', 'Davis', 'Developer', 'ISS', 'London', 'admin'],
           ['euser', 'Eric', 'Ericsson', 'Analyst', 'Analysis', 'London', 'admin'],
           ['fuser', 'Fabian', 'Fowles', 'Partner', 'IP', 'London', 'read']]
        
    LL_no_heads = [['auser', 'Arnold', 'Atkins', 'Partner', 'Tax', 'London', 'read'],
                    ['buser', 'Bill', 'Brown', 'Partner', 'Tax', 'New York', 'read'],
                    ['cuser', 'Clive', 'Cutler', 'Partner', 'Management', 'Brussels', 'read'],
                    ['duser', 'Denis', 'Davis', 'Developer', 'ISS', 'London', 'admin'],
                    ['euser', 'Eric', 'Ericsson', 'Analyst', 'Analysis', 'London', 'admin'],
                    ['fuser', 'Fabian', 'Fowles', 'IP', 'Partner', 'London', 'read']]

    #Example 1
    print "Example 1: Simple case, using defaults.\n"
    print LL2XML(LL)
    print "\n"
        
    #Example 2
    print """Example 2: LL has its headings in the first line, and we define our root and row element names.\n"""
    print LL2XML(LL,(),"people","person")
    print "\n"
    
    #Example 3
    print """Example 3: headings supplied using the headings argument(tuple), using default root and row element names.\n"""
    print LL2XML(LL_no_heads,("Login","First Name","Last Name","Job","Group","Office","Permission"))
    print "\n"
    
    #Example 4
    print """Example 4: The special case where we ask for an HTML table as output by just giving the string "table" as the second argument.\n"""
    print LL2XML(LL,"table")
