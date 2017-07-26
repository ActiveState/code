#!/usr/bin/env python
"""This is an mbox filter. It scans through an entire mbox style mailbox
and writes the messages to a new file. Each message is passed
through a filter function which may modify the document or ignore it.

The passthrough_filter() example below simply prints the 'from' email
address and returns the document unchanged. After running this script
the input mailbox and output mailbox should be identical.
"""

import mailbox, rfc822
import sys, os, string, re

LF = '\x0a'

def main ():
    mailboxname_in = sys.argv[1]
    mailboxname_out = mailboxname_in + '.out'
    process_mailbox (mailboxname_in, mailboxname_out, passthrough_filter)

def passthrough_filter (msg, document):
    """This prints the 'from' address of the message and
    returns the document unchanged.
    """
    from_addr = msg.getaddr('From')[1]
    print from_addr
    return document

def process_mailbox (mailboxname_in, mailboxname_out, filter_function):
    """This processes a each message in the 'in' mailbox and optionally
    writes the message to the 'out' mailbox. Each message is passed to
    the  filter_function. The filter function may return None to ignore
    the message or may return the document to be saved in the 'out' mailbox.
    See passthrough_filter().
    """

    # Open the mailbox.
    mb = mailbox.UnixMailbox (file(mailboxname_in,'r'))
    fout = file(mailboxname_out, 'w')

    msg = mb.next()
    while msg is not None:
        # Properties of msg cannot be modified, so we pull out the
        # document to handle is separately. We keep msg around to
        # keep track of headers and stuff.
        document = msg.fp.read()

        document = filter_function (msg, document)
        
        if document is not None:
            write_message (fout, msg, document)

        msg = mb.next()

    fout.close()

def write_message (fout, msg, document):
    """This writes an 'rfc822' message to a given file in mbox format.
    This assumes that the arguments 'msg' and 'document' were generate
    by the 'mailbox' module. The important thing to remember is that the
    document MUST end with two linefeeds ('\n'). It comes this way from
    the mailbox module, so you don't need to do anything if you want to
    write it unchanged. If you modified the document then be sure that
    it still ends with '\n\n'.
    """
    fout.write (msg.unixfrom)
    for l in msg.headers:
        fout.write (l)
    fout.write (LF)
    fout.write (document)

if __name__ == '__main__':
    main ()
