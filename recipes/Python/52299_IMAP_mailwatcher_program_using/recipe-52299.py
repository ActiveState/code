#!/usr/bin/env python
import imaplib, string, sys, os, re, rfc822
from Tkinter import *

PollInterval = 60 # seconds

def getimapaccount():
    try:
        f = open(os.path.expanduser('~/.imap'))
    except IOError, e:
        print 'Unable to open ~/.imap: ', e
        sys.exit(1)
    global imap_server, imap_user, imap_password
    try:
        imap_server, imap_user, imap_password = string.split(f.readline())
    except ValueError:
        print 'Invalid data in ~/.imap'
        sys.exit(1)
    f.close()

class msg: # a file-like object for passing a string to rfc822.Message
    def __init__(self, text):
	self.lines = string.split(text, '\015\012')
	self.lines.reverse()
    def readline(self):
	try: return self.lines.pop() + '\n'
	except: return ''

class Mailwatcher(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack(side=TOP, expand=YES, fill=BOTH)
        self.scroll = Scrollbar(self)
        self.list = Listbox(self, font='7x13',
                            yscrollcommand=self.scroll.set,
                            setgrid=1, height=6, width=80)
        self.scroll.configure(command=self.list.yview)
        self.scroll.pack(side=LEFT, fill=BOTH)
        self.list.pack(side=LEFT, expand=YES, fill=BOTH)

    def getmail(self):
	self.after(1000*PollInterval, self.getmail)
        self.list.delete(0,END)
	try:
	    M = imaplib.IMAP4(imap_server)
	    M.login(imap_user, imap_password)
	except Exception, e:
	    self.list.insert(END, 'IMAP login error: ', e)
	    return

	try:
	    result, message = M.select(readonly=1)
	    if result != 'OK':
		raise Exception, message
	    typ, data = M.search(None, '(UNSEEN UNDELETED)')
	    for num in string.split(data[0]):
		try:
		    f = M.fetch(num, '(BODY[HEADER.FIELDS (SUBJECT FROM)])')
		    m = rfc822.Message(msg(f[1][0][1]), 0)
		    subject = m['subject']
		except KeyError:
		    f = M.fetch(num, '(BODY[HEADER.FIELDS (FROM)])')
		    m = rfc822.Message(msg(f[1][0][1]), 0)
		    subject = '(no subject)'
		fromaddr = m.getaddr('from')
		if fromaddr[0] == "": n = fromaddr[1]
		else: n = fromaddr[0]
		text = '%-20.20s  %s' % (n, subject)
		self.list.insert(END, text)
	    len = self.list.size()
	    if len > 0: self.list.see(len-1)
	except Exception, e:
	    self.list.delete(0,END)
	    print sys.exc_info()
	    self.list.insert(END, 'IMAP read error: ', e)
	M.logout()


getimapaccount()
root = Tk(className='mailwatcher')
root.title('mailwatcher')
mw = Mailwatcher(root)
mw.getmail()
mw.mainloop()
