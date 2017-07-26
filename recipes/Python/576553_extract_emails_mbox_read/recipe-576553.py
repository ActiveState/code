'''
A simple mbox read-only mailbox generator.

Usage:
import sys
for msg in mboxo_generator(sys.stdin):
        print msg['Subject']
'''
# uncomment the following line on Python 2.2
#from __future__ import generators

import email.parser


def mboxo_generator(input, parser=email.parser.Parser()):
        '''Yield each message found in a ``input`` in ``mboxo`` / ``mboxrd`` format
        '''
        assert type(input) is file
        data = []
        for line in input:
                if line[:5] == 'From ' or line == '':
                        if data:
                                yield parser.parsestr(''.join(data))
                                data = []
                        elif line == '':
                                raise StopIteration
                data.append(line)


def mboxcl_generator(input, parser=email.parser.Parser()):
        '''Yield each message found in a ``input`` in ``mboxcl`` / ``mboxcl2`` format

        Do *not* use the "From " delimiter but *only* the ``Content-Lenght``
        header; in the case this field appear many times in the headers, the
        last one will prevail and if the field is missing an assertion might be raised.
        '''
        assert type(input) is file
        content_length = None
        length = 0
        in_header = None
        data = []
        for line in input:
                if in_header is None:
                        if line == '\n':
                                # eat empty lines before headers
                                # (usually between messages)
                                continue
                        in_header = True

                data.append(line)

                if in_header:
                        if line == '\n':
                                assert content_length is not None, 'header Content-Lenght not found (not an mboxcl file?)'
                                in_header = False
                        elif line[:16] == 'Content-Length: ':
                                content_length = int(line[16:].rstrip())
                else:
                        length+= len(line)
                        assert not length > content_length
                        if length == content_length:
                                yield parser.parsestr(''.join(data))
                                data = []
                                in_header = None
                                content_length = None
                                length = 0
        assert not length
