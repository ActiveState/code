#!/usr/bin/env python
import xml.dom.minidom as md
import sys

pretty_print = lambda f: '\n'.join([line for line in md.parse(open(f)).toprettyxml(indent=' '*2).split('\n') if line.strip()])

if __name__ == "__main__":
   if len(sys.argv)>=2:
      print pretty_print(sys.argv[1])
   else:
      sys.exit("Usage: %s [xmlfile]" % sys.argv[0])
