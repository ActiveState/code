#!/usr/local/bin/python
#
# This script is a helper to clean POP3 mailboxes
# containing malformed mails that hangs MUA's, that 
# are too large, or whatever...
#
# It iterates over the non-retrieved mails, prints
# selected elements from the headers and prompt the 
# user to delete bogus messages.
#
# Written by Xavier Defrang <xavier.defrang@brutele.be>
# 

# 
import getpass, poplib, re


# Change this to your needs
POPHOST = "pop.domain.com"
POPUSER = "jdoe"
POPPASS = ""

# How many lines of message body to retrieve
MAXLINES = 10

# Headers we're actually interrested in
rx_headers  = re.compile(r"^(From|To|Subject)")

try:

    # Connect to the POPer and identify user
    pop = poplib.POP3(POPHOST)
    pop.user(POPUSER)

    if not POPPASS:
        # If no password was supplied, ask for it
        POPPASS = getpass.getpass("Password for %s@%s:" % (POPUSER, POPHOST))

    # Authenticate user
    pop.pass_(POPPASS)

    # Get some general informations (msg_count, box_size)
    stat = pop.stat()

    # Print some useless information
    print "Logged in as %s@%s" % (POPUSER, POPHOST)
    print "Status: %d message(s), %d bytes" % stat

    bye = 0
    count_del = 0
    for n in range(stat[0]):

        msgnum = n+1

        # Retrieve headers
        response, lines, bytes = pop.top(msgnum, MAXLINES)

        # Print message info and headers we're interrested in
        print "Message %d (%d bytes)" % (msgnum, bytes)
        print "-" * 30
        print "\n".join(filter(rx_headers.match, lines))
        print "-" * 30

        # Input loop
        while 1:
            k = raw_input("(d=delete, s=skip, v=view, q=quit) What?")
            if k in "dD":
                # Mark message for deletion
                k = raw_input("Delete message %d? (y/n)" % msgnum)
                if k in "yY":
                    pop.dele(msgnum)
                    print "Message %d marked for deletion" % msgnum
                    count_del += 1
                break
            elif k in "sS":
                print "Message %d left on server" % msgnum
                break
            elif k in "vV":
                print "-" * 30
                print "\n".join(lines)
                print "-" * 30
            elif k in "qQ":
                bye = 1
                break

        # Time to say goodbye?    
        if bye:
            print "Bye"
            break

    # Summary
    print "Deleting %d message(s) in mailbox %s@%s" % (count_del, POPUSER, POPHOST)

    # Commit operations and disconnect from server
    print "Closing POP3 session"
    pop.quit()

except poplib.error_proto, detail:

    # Fancy error handling
    print "POP3 Protocol Error:", detail
