#!/usr/local/bin/python
# 2002-05-19 - fsf
# last modified: 2002-06-16

import sys, re, string
import poplib
from poplib import *

pop_host = 'insert_pop3_server_here'
pop_user = 'insert_username_here'
pop_pass = 'insert_password_here'

filter_size = 50000
if len (sys.argv) > 1:
    filter_size = sys.argv[1]

p = POP3 (pop_host)
p.user (pop_user)
p.pass_ (pop_pass)

[msgs, psize] = p.stat ()
if msgs < 1:
    print 'No messages found in mailbox ... exiting!'
    sys.exit (0)
else:
    print msgs, 'found with a total size of', psize, 'octets...'

re_from = re.compile ("^From:")
re_to = re.compile ("^To:")
re_subject = re.compile ("^Subject:")

filtered = []

for pid in range (1, msgs + 1):
    h_from = h_to = h_subject = ''

    list_fields = string.split (p.list (pid))
    size = list_fields[2]
    if int (size) < int (filter_size):
        continue

    filtered.append (pid)

    top = p.top (pid, 0)
    headers = top[1]
    for line in headers:
        if re_from.match (line):
            h_from = line
        elif re_to.match (line):
            h_to = line
        elif re_subject.match (line):
            h_subject = line

    print 'Message %d (%s octets)' % (pid, size)
    print h_from
    print h_to
    print h_subject
    print

input = raw_input ("Delete Messages [1 - %d, (A)ll Filtered, (Q)uit]: " \
    % (msgs))

input = string.lower (input)

if (input == 'all') or (input == 'a'):
    print 'Deleting all messages larger than %s bytes...' % (filter_size)
    delete = filtered
    # delete = range (1, msgs + 1)
elif (input == 'q'):
    sys.exit (0)
else:
    delete = string.split (input)

for pid in delete:
    print 'Deleting message %s...' % pid
    p.dele (pid)

p.quit ()
