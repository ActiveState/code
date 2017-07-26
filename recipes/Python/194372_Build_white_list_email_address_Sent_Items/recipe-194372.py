#!/usr/bin/env python
"""This extracts all of the To addresses from an mbox file.
    It is used on a "Sent Items" mailbox to build an address white list.
"""
import mailbox
import sys

MAILBOXIN = sys.argv[1]

def main ():

    addr_list = []
    mb = mailbox.UnixMailbox (file(MAILBOXIN,'r'))
    for msg in mb:
        toaddr = msg.getaddr('To')[1]
        if toaddr not in addr_list:
            addr_list.append (toaddr)

    addr_list.sort()
    for addr in addr_list:
        print addr

if __name__ == '__main__':
    main ()
