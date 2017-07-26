#!/usr/bin/env python

import sys
from ldif import LDIFParser, LDIFWriter

basedn = 'ou=contacts,dc=linuxkorea,dc=co,dc=kr'

ignore_attribute = [
    'modifytimestamp',
    ]

copy_attribute = [
    ['sn', 'cn'],
    ]

ignore_objectclass = [
    'organizationalPerson',
    'mozillaAbPersonObsolete',
    ]

class FixLDIF(LDIFParser):
    def __init__(self, input, output):
        LDIFParser.__init__(self, input)
        self.writer = LDIFWriter(output)
    def handle(self, dn, entry):
        dn = self.fix_dn(dn)
        self.fix_entry(entry)
        self.fix_objectclass(entry['objectclass'])
        self.writer.unparse(dn, entry)
    def fix_dn(self, dn):
        head = dn.split(',', 1)[0]
        return head + ',' + basedn
    def fix_entry(self, entry):
        for value in ignore_attribute:
            if value in entry:
                del entry[value]
        for target, source in copy_attribute:
            entry[target] = entry[source]
    def fix_objectclass(self, objectclass):
        for value in ignore_objectclass:
            if value in objectclass:
                objectclass.remove(value)

if len(sys.argv) != 3:
    print sys.argv[0], 'input.ldif', 'output.ldif'
    sys.exit()

input = open(sys.argv[1], 'r')
output = open(sys.argv[2], 'w')
parser = FixLDIF(input, output)
parser.parse()
