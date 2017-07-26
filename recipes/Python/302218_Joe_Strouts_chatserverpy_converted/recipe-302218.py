#!/usr/bin/env python

# A simple 94(*) lines of code "chat" server.  Creates a server on port 4000.
# Users telnet to your machine, at port 4000, and can chat with each other.
# Use "quit" to disconnect yourself, and "shutdown" to shut down the server.
#
# Adapted from J. Strout version at 
# http://www.strout.net/info/coding/python/tidbits.html#server 

# Modified by me (Steve <lonetwin@yahoo.com>) as a follow-up assignment for
# a basic python lecture I conducted.
# 
# Instructions: I have put various comments in the code.
#       Some comments are preceded with the marker [Tip]. These comments
#   explain some coding-style rules that might commonly be seen in python code.
#       Some comments are preceded with the marker [n], where 'n' is a number.
#   These comments have questions that have to be answered by mail to me.
#   Please write the question number before the answer. To find the answers to
#   these questions you may have to read the python documentation or search the
#   web. In any case, feel free to contact me if you find any that are hard to
#   answer.
#       The comments at the bottom of the file are enhancements to this
#   program. You are expected to write these on your own. You are free to use
#   any references, including any code that you might find on the net for this
#   purpose, with the only condition being that you should credit the source
#   when you hand in the assignment.
#

from socket import *    # [1] What does this statement do ? 
import time             # [2] How does this statement differ from the previous?
                        # [Tip] Read Chap. 6 of the official Python Tutorial

# define global variables
HOST = ''               # [Tip] In the socket module, an empty string for the
                        #       hostname by default maps to 'localhost'
PORT = 4000             # [3] Can I use 40 here instead ? why ?
endl = "\r\n"           # [4] What is this character sequence and why has
                        #     it been defined separately ?

userlist = []           # list of connected users

# some constants used to flag the state of user
kAskName, kWaitName, kOK = 0, 1, 2 

# [5] What is the scope of all the variables defined above ?
# [Tip] Read section 9.2 of the official Python Tutorial

class User:
    """
    class to store info about connected users
    """
    def __init__(self, conn, addr):
        self.conn, self.addr = conn, addr
        self.name, self.step = "", kAskName

    def poll(self):
        if self.step == kAskName: self.AskName()
        # [Tip] blocks with single statements need not be written on an
        #       indented line.

    def AskName(self):
        self.conn.send("Name? ")
        self.step = kWaitName

    def HandleMsg(self, msg):
        print "Handling message: %s" % msg
        global userlist # [6] What is the purpose of this statement ?
        # if waiting for name, record it
        if self.step == kWaitName:
            # try to trap initial garbage sent by some telnet programs ...
            if len(msg) < 2 or msg == "#": return
            print "Setting name to: %s" % msg
            self.name, self.step = msg, kOK
            self.SendMsg("Hello, %s" % self.name)
            broadcast("%s has connected." % self.name)
            return
        if msg == "quit":       # check for commands
            broadcast("%s has quit." % self.name)
            self.conn.close()
            userlist.remove(self)
        else:                   # otherwise, broadcast msg
            broadcast("%s: %s" % (self.name, msg))

    def SendMsg(self, msg):
        self.conn.send(msg + endl)
        
def pollNewConn(s):
    """
    Routine to check for incoming connections. Accepts a socket object 's' as
    argument and returns a User object 'user'
    """
    try:
        conn, addr = s.accept()     # [Tip] Read the socket HOWTO
    except:
        return None
    print "Connection from ", addr
    conn.setblocking(0)             # [7] What is the effect of this call ?
    user = User(conn, addr)
    return user

def broadcast(msg): # [8] Does this belong to the User class ?? support your
                    #     answer with sufficient reasoning.
    """
    Routine to broadcast a message to all connected users. Takes the argument
    message 'msg', in the form '<sender>: <message>'
    """
    map(lambda u: u.SendMsg(msg), \
        filter(lambda u: u.name != msg.split(':')[0], \
               userlist))
    # [9] Convert the above map+lambda+filter into a readable loop+conditional

# Main Program
def main():
    # set up the server
    s = socket(AF_INET, SOCK_STREAM)
    s.bind((HOST, PORT))
    s.setblocking(0)
    s.listen(1)
    print "Waiting for connection(s)..."

    # loop until done, handling connections and incoming messages
    done = 0                        # set to 1 to shut this down
    while not done:
        try:
            time.sleep(1)           # sleep to reduce processor usage
            u = pollNewConn(s)      # check for incoming connections
            if u:
                userlist.append(u)
                print "%d connection(s)" % len(userlist)

            for u in userlist:      # check all connected users
                u.poll()
                try:
                    data = u.conn.recv(1024)
                    data = filter(lambda x: x >= ' ' and x <= 'z', data)
                    # [10] Rewrite the above statement as a List Comprehension.
                    data = data.strip()
                    if data:
                        print "From %s: [%s]" % (u.name, data)
                        u.HandleMsg(data)
                        if data == "shutdown": done=1
                except:
                    pass    # [11] What exception are we ignoring ? and why ?
        except KeyboardInterrupt:
            done=1
    else:                           # [12] What does this statement imply ?
        print "Shutting down ..."   # [Tip] Read section 4.4 of the official
        s.shutdown(2)               #       Python Tutorial
        s.close()

    # We are done, close all connections
    for u in userlist:
        u.conn.close()

if __name__ == '__main__':  # [Tip] Read about the if __name__ == '__main__'
    main()                  #       trick in chap. 2 at diveintopython.org

# Rewrite the server program to do the following things:
# a) Log it's status/action messages (*not* the actual chat msgs) to a log
#    file as well as print it out to the console.
# b) Enhance the User class to recognize more commands besides 'quit'.
#    [Tip] We can implement this using a 'dispatcher' for example, I should be
#          able to do something like this in the HandleMsg method:
#       if msg in commands:
#           cmd = getattr(self, command)
#           cmd()
# c) Design and implement a client for this server.
# d) Take care of the problem in question no. [11]
#    [Tip] Read section 5 of the Python Socket Programming HOWTO.    
# e) Create a chat client/server package
#    [Tip] Read 6.4 of the Official Python Tutorial

# (*) 94 == `egrep -v "(^[ ]*#)|(^[ ]*$)" chat_server.py | wc -l`
# vim: set tw=80 et ai sts=4 sw=4 ts=8:
