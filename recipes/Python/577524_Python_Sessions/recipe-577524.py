#!/usr/local/bin/python26
"""
Python Session Handling

Note: A user must have cookies enabled!

TODO:
* Support Named Sessions

Copyright 2010 - Sunjay Varma

Latest Version: http://www.sunjay.ca/download/session.py
"""

import cgi
import os
import time
import errno
import hashlib
import datetime

from Cookie import SimpleCookie
from cPickle import dump, load, HIGHEST_PROTOCOL, dumps, loads

if not "HTTP_COOKIE" in os.environ:
	os.environ["HTTP_COOKIE"] = ""

SESSION = None

S_DIR = os.path.expanduser("~/.py_sessions") # expanduser for windows users
S_EXT = ".ps"
S_ID = "__sid__"

TODAY = str(datetime.date.today())
DEBUG = [] # debug messages

if not os.path.exists(S_DIR):
	os.makedirs(S_DIR)

class NoCookiesError(Exception): pass
class NotStarted(Exception): pass

class Session(object):

	def __init__(self):
		self.data = {}
		self.started = False
		self._flock = None
		self.expires = 0 # delete right away
		
		self.__sid = sid = self.__getsid()
		self.path = os.path.join(S_DIR, sid+S_EXT)

	def isset(self, name):
		"""Is the variable set in the session?"""
		if not self.started:
			raise NotStarted("Session must be started")

		return name in self

	def unset(self, name):
		"""Unset the name from the session"""
		if not self.started:
			raise NotStarted("Session must be started")
		del self[name]

	@staticmethod
	def __newsid():
		"""Create a new session ID"""
		h = hashlib.new("ripemd160")
		h.update(str(time.time()/time.clock()**-1)+str(os.getpid()))
		return h.hexdigest()

	def __getsid(self):
		"""Get the current session ID or return a new one"""
		# first, try to load the sid from the GET or POST forms
		form = cgi.FieldStorage()
		if form.has_key(S_ID):
			sid = form[S_ID].value
			return sid

		# then try to load the sid from the HTTP cookie
		self.cookie = SimpleCookie()
		if os.environ.has_key('HTTP_COOKIE'):
			self.cookie.load(os.environ['HTTP_COOKIE'])

			if S_ID in self.cookie:
				sid = self.cookie[S_ID].value
				return sid
		else:
			raise NoCookiesError("Could not find any cookies")

		# if all else fails, return a new sid
		return self.__newsid()

	def getsid(self):
		"""
		Return the name and value that the sid needs to have in a GET or POST
		request
		"""
		if not self.started:
			raise NotStarted("Session must be started")
		return (S_ID, self.__sid)

	def start(self):
		"""Start the session"""
		if self.started:
			return True # session cannot be started more than once per script

		self._flock = FileLock(self.path)
		self._flock.acquire()

		# load the session if it exists
		if os.path.exists(self.path):
			with open(self.path, "rb") as f:
				self.data = dict(load(f))
				self.data["__date_loaded__"] = TODAY

		else: # create a session
			with open(self.path, "wb") as f:
				self.data = {"__date_loaded__":TODAY}

		# the session is officially started!
		self.started = True

		# store the sid in the cookie
		self.cookie[S_ID] = self.__sid
		self.cookie[S_ID]["expires"] = str(self.expires)
		self.cookie[S_ID]["version"] = "1"

		return True

	def commit(self):
		"""Commit the changes to the session"""
		if not self.started:
			raise NotStarted("Session must be started")
		with open(self.path, "wb") as f:
			dump(self.data, f, HIGHEST_PROTOCOL)

	def destroy(self):
		"""Destroy the session"""
		if not self.started:
			raise NotStarted("Session must be started")
		os.delete(self.path)
		if self._flock:
			self._flock.release()
		self.started = False

	def output(self):
		"""Commit changes and send headers."""
		if not self.started:
			raise NotStarted("Session must be started")
		self.commit()
		return self.cookie.output()

	def setdefault(self, item, default=None):
		if not self.started:
			raise NotStarted("Session must be started")
		if not self.isset(item):
			self[item] = default

		return self[item]
		
	def set_expires(self, days):
		"""Sets the expiration of the cookie"""
		date = datetime.date.today() + datetime.timedelta(days=days)
		self.expires = date.strftime("%a, %d-%b-%Y %H:%M:%S PST")
		self.cookie[S_ID]["expires"] = str(self.expires)

	def __getitem__(self, item):
		"""Get the item from the session"""
		if not self.started:
			raise NotStarted("Session must be started")
		return self.data.__getitem__(item)

	def __setitem__(self, item, value):
		"""set the item into the session"""
		if not self.started:
			raise NotStarted("Session must be started")
		self.data.__setitem__(item, value)

	def __delitem__(self, item):
		if not self.started:
			raise NotStarted("Session must be started")
		self.data.__delitem__(item)

	def __contains__(self, item):
		"""Return if item in the session"""
		if not self.started:
			raise NotStarted("Session must be started")
		return self.data.__contains__(item)

	def __iter__(self):
		"""Go through the names of all the session variables"""
		if not self.started:
			raise NotStarted("Session must be started")
		return self.data.__iter__()

def start():
	global SESSION
	SESSION = Session()
	return SESSION.start()

def destroy():
	global SESSION
	if SESSION:
		SESSION.destroy()

def get_session():
	global SESSION
	if not SESSION:
		SESSION = Session()
	return SESSION

### The following is a (little) modified version of this:
# http://www.evanfosmark.com/2009/01/cross-platform-file-locking-support-in-
# python/

class FileLockException(Exception):
	pass

class FileLock(object):
	""" A file locking mechanism that has context-manager support so
		you can use it in a with statement. This should be relatively cross
		compatible as it doesn't rely on msvcrt or fcntl for the locking.
	"""

	def __init__(self, file_name, timeout=10, delay=.05):
		""" Prepare the file locker. Specify the file to lock and optionally
			the maximum timeout and the delay between each attempt to lock.
		"""
		self.is_locked = False
		self.lockfile = os.path.join(os.getcwd(), "%s.lock" % file_name)
		self.file_name = file_name
		self.timeout = timeout
		self.delay = delay

	def acquire(self):
		""" Acquire the lock, if possible. If the lock is in use, it check again
			every `wait` seconds. It does this until it either gets the lock or
			exceeds `timeout` number of seconds, in which case it throws
			an exception.
		"""
		if self.is_locked:
			return

		start_time = time.time()
		while True:
			try:
				self.fd = os.open(self.lockfile, os.O_CREAT|os.O_EXCL|os.O_RDWR)
				break;
			except OSError as e:
				if e.errno != errno.EEXIST:
					raise

				if (time.time() - start_time) >= self.timeout:
					raise FileLockException("Timeout occured.")
				time.sleep(self.delay)
		self.is_locked = True

	def release(self):
		""" Get rid of the lock by deleting the lockfile.
			When working in a `with` statement, this gets automatically
			called at the end.
		"""
		if self.is_locked:
			os.close(self.fd)
			os.unlink(self.lockfile)
			self.is_locked = False

	def __enter__(self):
		""" Activated when used in the with statement.
			Should automatically acquire a lock to be used in the with block.
		"""
		if not self.is_locked:
			self.acquire()
		return self

	def __exit__(self, type, value, traceback):
		""" Activated at the end of the with statement.
			It automatically releases the lock if it isn't locked.
		"""
		if self.is_locked:
			self.release()

	def __del__(self):
		""" Make sure that the FileLock instance doesn't leave a lockfile
			lying around.
		"""
		self.release()

def print_session(session):
	"""
	Prints info from the current session.

	WARNING: ONLY FOR DEBUGGING. MAJOR SECURITY RISK!
	"""
	print "<h3>Session Data</h3>"
	print "<dl>"
	for name in session:
		print "<dt>%s <i>%s</i></dt>"%(name, type(session[name]))
		print "<dd>%s</dd>"%repr(session[name])
	print "</dl>"

def main():
	"""Tester Program"""

	start() # session.start()
	if SESSION.isset("views"):
		SESSION["views"] += 1
	else:
		SESSION["views"] = 1

	print "Content-type: text/html"
	print SESSION.output()
	print

	print "<html><head><title>Session Testing</title></head><body>"
	print "<h2>You have viewed this page %i times.</h2>"%SESSION["views"]
	print_session(SESSION)
	print "<p>", SESSION.path, "</p>"
	for line in DEBUG:
		print "<p>%s</p>"%line
	print "<p>%s</p>"%SESSION.data
	print "</body></html>"

if __name__ == "__main__":
	main()
