#!/usr/bin/env python

import base64
import sys

encode_or_decode = 'encode' in sys.argv[0].lower() and base64.encode or 'decode' in sys.argv[0].lower() and base64.decode or (sys.stderr.write("Error: script name must contain 'encode' or 'decode'!\n") or sys.exit(-1))

encode_or_decode(len(sys.argv) > 1 and open(sys.argv[1]) or sys.stdin, len(sys.argv) > 2 and open(sys.argv[2],'w') or sys.stdout)
