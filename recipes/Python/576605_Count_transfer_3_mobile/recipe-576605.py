#!/usr/bin/python

doc="""
Usage examples:

phone_data Jan  2 2009 08:42:13
phone_data
"""

from dateutil import parser
from dateutil.parser import parse
import sys

if len(sys.argv) > 1:
    if sys.argv[1] in ['-h', '--help']:
        print doc
        sys.exit()
    start_date = parse(' '.join(sys.argv[1:]))
else:
    start_date = None

f=file('/var/log/ppp.log')
sent = []
recv = []

in_phoneblock=False
for line in f:
    if line.find('Dialing: ATD*99***1#') > 0:
        if start_date is not None:
            this_date = parse(line.split(' : ')[0])
            if this_date > start_date:
                in_phoneblock = True
        else:
            in_phoneblock = True
    if in_phoneblock and line.find('Sent') > 0:
        print line,
        info=line.split(':')[3].split(' ')
        sent.append(int(info[2]))
        recv.append(int(info[5]))
        in_phoneblock = False
print '\nTOTALS: Sent: %i mb, received: %i mb, total: %i mb.\n'%(sum(sent)/1.e6, sum(recv)/1.e6, (sum(sent)+sum(recv))/1.e6)
