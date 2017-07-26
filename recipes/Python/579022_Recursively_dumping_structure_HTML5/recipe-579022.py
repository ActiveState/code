# Demo program to show how to dump the structure of 
# an HTML5 document to text, using html5lib.
# Author: Vasudev Ram.
# Copyright 2015 Vasudev Ram - http://www.dancingbison.com

import html5lib

# Define a function to dump HTML5 element info recursively, 
# given a top-level element.
def print_element(elem, indent, level):
    for sub_elem in elem:
        print "{}{}".format(indent * level, sub_elem)
        # Recursive call to print_element().
        print_element(sub_elem, indent, level + 1)

f = open("html5doc.html")
# Parse the HTML document.
tree = html5lib.parse(f)
indent = '----'
level = 0
print_element(tree, indent, level)
