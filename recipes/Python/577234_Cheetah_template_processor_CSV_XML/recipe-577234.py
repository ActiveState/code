#!/usr/bin/python

import  getopt, sys

usage="""
    This script will populate a Cheetah template ((http://www.cheetahtemplate.org/) 
    with some input data (XML, CSV or JSON format).

    By default, the output is directed to stdout.

    USAGE:
        template [ -o outputFile ] [options] <template_file> <data_file> 
        template [-h/--help] 

    ARGUMENTS:
        <template_file> : Filename for the template file. Can be "stdin"
        <data_file> : Filename for input data. Can be "stdin"

    OPTIONS:
        -o <output file>   Direct output in a file instead of stdout.              
        -c 'commentChar'   Change the character used to begin comments in the template.
        -d 'directiveChar' Change the character used for directives in the template.
        -t XML|CSV         Input type (or guessed with file extension)

"""


def dieWith(msg) :
    sys.stderr.write(msg + '\n')
    sys.exit(-1)

# Enum of data type
TYPE_NONE = 0
TYPE_XML = 2
TYPE_CSV = 3

# Parse options
try:
    opts, args = getopt.getopt(sys.argv[1:], "hc:d:t:o:", ["help"])
except getopt.GetoptError :
    print usage

# Init arguments / options
compilerSettings = {}
inputType = TYPE_NONE
outFilename = None

# Switch on options
for opt, arg in opts:

    # Help
    if opt in ("-h", "--help") :
        print usage
        sys.exit(0)

    # Comment char
    elif opt == "-c" :
        compilerSettings['commentStartToken'] = arg

    # Directive char
    elif opt == "-d" :
        compilerSettings['directiveStartToken'] = arg

    # Output file
    elif opt == "-o" :
        outFilename = arg

    # Input type
    elif opt == "-t" :
        arg= arg.lower()
        if arg == "csv" :
            inputType = TYPE_CSV
        elif arg == "xml" :
            inputType = TYPE_XML
        else :
            dieWith("Invalid input type. Valid options are : CSV, XML")
            
# 2 mandatory arguments    
if len(args) != 2:
    print usage
    sys.exit(2);

(templateFile, dataFile) = args

# --------------------------------------------------------------------------
# XML to Python Object parser
# --------------------------------------------------------------------------
## {{{ http://code.activestate.com/recipes/534109/ (r8)
## Created by Wai Yip Tung on Sat, 13 Oct 2007 

import re
import xml.sax.handler

def xml2obj(src):
    """
    A simple function to converts XML data into native Python object.
    """

    non_id_char = re.compile('[^_0-9a-zA-Z]')
    def _name_mangle(name):
        return non_id_char.sub('_', name)

    class DataNode(object):
        def __init__(self):
            self._attrs = {}    # XML attributes and child elements
            self.data = None    # child text data
        def __len__(self):
            # treat single element as a list of 1
            return 1
        def __getitem__(self, key):
            if isinstance(key, basestring):
                return self._attrs.get(key,None)
            else:
                return [self][key]
        def __contains__(self, name):
            return self._attrs.has_key(name)
        def __nonzero__(self):
            return bool(self._attrs or self.data)
        def __getattr__(self, name):
            if name.startswith('__'):
                # need to do this for Python special methods???
                raise AttributeError(name)
            return self._attrs.get(name,None)
        def _add_xml_attr(self, name, value):
            if name in self._attrs:
                # multiple attribute of the same name are represented by a list
                children = self._attrs[name]
                if not isinstance(children, list):
                    children = [children]
                    self._attrs[name] = children
                children.append(value)
            else:
                self._attrs[name] = value
        def __str__(self):
            return self.data or ''
        def __repr__(self):
            items = sorted(self._attrs.items())
            if self.data:
                items.append(('data', self.data))
            return u'{%s}' % ', '.join([u'%s:%s' % (k,repr(v)) for k,v in items])

    class TreeBuilder(xml.sax.handler.ContentHandler):
        def __init__(self):
            self.stack = []
            self.root = DataNode()
            self.current = self.root
            self.text_parts = []
        def startElement(self, name, attrs):
            self.stack.append((self.current, self.text_parts))
            self.current = DataNode()
            self.text_parts = []
            # xml attributes --> python attributes
            for k, v in attrs.items():
                self.current._add_xml_attr(_name_mangle(k), v)
        def endElement(self, name):
            text = ''.join(self.text_parts).strip()
            if text:
                self.current.data = text
            if self.current._attrs:
                obj = self.current
            else:
                # a text only node is simply represented by the string
                obj = text or ''
            self.current, self.text_parts = self.stack.pop()
            self.current._add_xml_attr(_name_mangle(name), obj)
        def characters(self, content):
            self.text_parts.append(content)

    builder = TreeBuilder()
    if isinstance(src,basestring):
        xml.sax.parseString(src, builder)
    else:
        xml.sax.parse(src, builder)
    return builder.root._attrs.values()[0]

## end of http://code.activestate.com/recipes/534109/ }}}




# -------------------------------------------------
# Read input data file
# -------------------------------------------------

# Open input file
import csv
if dataFile == "stdin" :
    file = sys.stdin
else:
    file = open(dataFile);
        
    # Guess input type if not set in options
    if inputType == TYPE_NONE :
        import os.path as path
        ext = path.splitext(dataFile)[1].lower()

        if ext == '.csv' :
            inputType = TYPE_CSV
        elif ext == '.xml' :
            inputType = TYPE_XML 
        elif ext == '.json' :
            inputType = TYPE_JSON

# Switch on input type
if inputType == TYPE_NONE :
    dieWith("No input data type specified. Failed to guess it.")

# CSV
elif inputType == TYPE_CSV :

    reader = csv.DictReader(file, delimiter=";")

    # Almost empty 
    class Container :
        def __init__(self) :
            self.lines= []

    data = Container()

    # Loop on lines
    for line in reader:

        data.lines.append(line)

        # Loop on values of the line
        for key, value in line.items() :
           
            # Does it exists yet in "data"
            if data.__dict__.has_key(key) :
                # Then happend it
                data.__dict__[key].append(value)
            else :
                # Create a list 
                data.__dict__[key] = [value]

    # Make 'columns' accessible as a global name in the template
    data.columns = reader.fieldnames

# XML
elif inputType == TYPE_XML :
    
    # Transform XML into Python object
    data = xml2obj(file)

else :
    dieWith('Input data type not supported')

# --------------------------------------------
# Read template
# --------------------------------------------

from Cheetah.Template import Template
if templateFile == 'stdin' :
    file = sys.stdin
else:
    file = open(templateFile)

template = Template(
    file=file, 
    searchList=[data], # Attach data
    compilerSettings = compilerSettings)

# -------------------------------------------
# Output result
# -------------------------------------------

if outFilename == None :
    out = sys.stdout
else :
    out = open(outFilename, 'w')

out.write(str(template))
