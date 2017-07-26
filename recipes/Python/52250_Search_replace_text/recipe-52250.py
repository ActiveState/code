#!/usr/bin/env python
import os, sys
usage = "usage: %s search_text replace_text [infile [outfile]]" %         os.path.basename(sys.argv[0])

if len(sys.argv) < 3:
    print usage
else:
    stext = sys.argv[1]
    rtext = sys.argv[2]
    input = sys.stdin
    output = sys.stdout
    if len(sys.argv) > 3:
        input = open(sys.argv[3])
    if len(sys.argv) > 4:
        output = open(sys.argv[4], 'w')
    for s in input.xreadlines():
        output.write(s.replace(stext, rtext))


  # For older versions of Python (1.5.2 and earlier) import
  # the string module and replace the last two lines with:
  #
  # for s in input.readlines():
  #     output.write(string.replace(s, stext, rtext))
