'''
Py2XML - Python to XML serialization

This code transforms a Python data structures into an XML document

Usage:
    serializer = Py2XML()
    xml_string = serializer.parse( python_object )
    print python_object
    print xml_string
'''

class Py2XML():

    def __init__( self ):

        self.data = "" # where we store the processed XML string

    def parse( self, pythonObj, objName=None ):
        '''
        processes Python data structure into XML string
        needs objName if pythonObj is a List
        '''
        if pythonObj == None:
            return ""

        if isinstance( pythonObj, dict ):
            self.data = self._PyDict2XML( pythonObj )
            
        elif isinstance( pythonObj, list ):
            # we need name for List object
            self.data = self._PyList2XML( pythonObj, objName )
            
        else:
            self.data = "<%(n)s>%(o)s</%(n)s>" % { 'n':objName, 'o':str( pythonObj ) }
            
        return self.data

    def _PyDict2XML( self, pyDictObj, objName=None ):
        '''
        process Python Dict objects
        They can store XML attributes and/or children
        '''
        tagStr = ""     # XML string for this level
        attributes = {} # attribute key/value pairs
        attrStr = ""    # attribute string of this level
        childStr = ""   # XML string of this level's children

        for k, v in pyDictObj.items():

            if isinstance( v, dict ):
                # child tags, with attributes
                childStr += self._PyDict2XML( v, k )

            elif isinstance( v, list ):
                # child tags, list of children
                childStr += self._PyList2XML( v, k )

            else:
                # tag could have many attributes, let's save until later
                attributes.update( { k:v } )

        if objName == None:
            return childStr

        # create XML string for attributes
        for k, v in attributes.items():
            attrStr += " %s=\"%s\"" % ( k, v )

        # let's assemble our tag string
        if childStr == "":
            tagStr += "<%(n)s%(a)s />" % { 'n':objName, 'a':attrStr }
        else:
            tagStr += "<%(n)s%(a)s>%(c)s</%(n)s>" % { 'n':objName, 'a':attrStr, 'c':childStr }

        return tagStr

    def _PyList2XML( self, pyListObj, objName=None ):
        '''
        process Python List objects
        They have no attributes, just children
        Lists only hold Dicts or Strings
        '''
        tagStr = ""    # XML string for this level
        childStr = ""  # XML string of children

        for childObj in pyListObj:
            
            if isinstance( childObj, dict ):
                # here's some Magic
                # we're assuming that List parent has a plural name of child:
                # eg, persons > person, so cut off last char
                # name-wise, only really works for one level, however
                # in practice, this is probably ok
                childStr += self._PyDict2XML( childObj, objName[:-1] )
            else:
                for string in childObj:
                    childStr += string;

        if objName == None:
            return childStr

        tagStr += "<%(n)s>%(c)s</%(n)s>" % { 'n':objName, 'c':childStr }

        return tagStr


def main():

    python_object = {'documents': [{'formats': [{'info': {'uri': 'http://www.python.org/newness-of-python.pdf', 'pages': '245'}, 'type': 'pdf'}, {'info': {'uri': 'http://www.python.org/newness-of-python.html'}, 'type': 'web'}], 'copyright': {'url': 'http://www.creativecommons.org/', 'date': 'June 24, 2009', 'type': 'CC'}, 'title': 'The Newness of Python', 'date': 'June 6, 2009', 'text': ['Python is very nice. Very, very nice.'], 'author': 'John Doe'}]}
    
    serializer = Py2XML()
    xml_string = serializer.parse( python_object )
    print python_object
    print xml_string


if __name__ == '__main__':
    main()
