#!/usr/bin/python

import sys
import getpass
import poplib

def popPeek(server, user, port=110):

    try:
        P = poplib.POP3(server, port)
        P.user(user)
        P.pass_(getpass.getpass())
    except:
        print "Failed to connect to server."
        sys.exit(1)

    deleted = 0

    try:
        l = P.list()
        msgcount = len(l[1])
        for i in range(msgcount):
            msg = i+1
            top = P.top(msg, 0)
            for line in top[1]:
                print line
            input = raw_input("D to delete, any other key to leave message on server: ")
            if input=="D":
                P.dele(msg)
                deleted += 1
        P.quit()                
        print "%d messages deleted. %d messages left on server" % (deleted, msgcount-deleted)
    except:
        P.rset()
        P.quit()
        deleted = 0
        print "\n%d messages deleted. %d messages left on server" % (deleted, msgcount-deleted)

if __name__ == "__main__":

    if len(sys.argv)<3:
        print """
Usage: popPeek.py server username [port]
        """
    else:
        popPeek(sys.argv[1], sys.argv[2], sys.argv[3])
