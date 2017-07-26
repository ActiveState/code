#!/usr/bin/env python

# updated 2005.07.21, thanks to Jacob Oscarson
# updated 2006.03.30, thanks to Mark Eichin

import sys
import re
import getopt

# parse options for module imports
opts, args = getopt.getopt(sys.argv[1:], 'm:')
opts = dict(opts)
if '-m' in opts:
    for imp in opts['-m'].split(','):
        locals()[imp] = __import__(imp.strip())

cmd = ' '.join(args)
if not cmd.strip():
    cmd = 'line'                        # no-op
    
codeobj = compile(cmd, 'command', 'eval')
write = sys.stdout.write

for numz, line in enumerate(sys.stdin):
    line = line[:-1]
    num = numz + 1
    words = [w for w in line.strip().split(' ') if len(w)]
    result =  eval(codeobj, globals(), locals())
    if result is None or result is False:
        continue
    elif isinstance(result, list) or isinstance(result, tuple):
        result = ' '.join(map(str, result))
    else:
        result = str(result)
    write(result)
    if not result.endswith('\n'):
        write('\n')
