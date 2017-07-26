#!/usr/bin/python

# Import
import xml.etree.ElementTree as ET
import sys


def removeNS(tag) :
    if tag.find('}') == -1 :
        return tag
    else:
        return tag.split('}', 1)[1]

def linearize(el, path) :

    # Print text value if not empty
    text = el.text.strip()
    if text == "" :
        print path  
    else :

        # Several lines ?
        lines = text.splitlines()
        if len(lines) > 1 :
            lineNb=1
            for line in lines :
                print path + "[line %d]=%s " % (lineNb, line)
                lineNb += 1
        else :
            print path + "=" + text
    

    # Print attributes
    for name, val in el.items() :
        print path + "/@" + removeNS(name) + "=" + val

    # Counter on the sibbling element names
    counters = {}

    # Loop on child elements
    for childEl in el :

        # Remove namespace
        tag = removeNS(childEl.tag)

        # Tag name already encountered ?
        if counters.has_key(tag) :
            counters[tag] += 1
            # Number it
            numberedTag = tag + "[" + str(counters[tag]) + "]"
        else :
            counters[tag] = 1
            numberedTag = tag

        # Print child node recursively
        linearize(childEl, path + '/' + numberedTag)

# Main 
def process(stream, prefix) :

    # Parse the XML
    tree = ET.parse(stream)

    # Get root element
    root = tree.getroot()

    # Linearize
    linearize(root, prefix + "//" + removeNS(root.tag))


# Each argument is a file
args = sys.argv[1:]

# Loop on files
for filename in args :

    # Open the file
    file = open(filename)
    
    # If we process several files, prefix each one with its path
    if len(args) > 1 :
        prefix = filename + ":"
    else:
        prefix = ""

    # Process it
    process(file, prefix)

# No input file ? => Proces std input
if len(args) == 0 :
    process(sys.stdin, "") 
