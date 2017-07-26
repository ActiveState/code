from select import epoll, EPOLLIN, EPOLLOUT, EPOLLERR, EPOLLHUP
from subprocess import Popen, PIPE
import errno, fcntl
from time import time
import os, sys

# Exit conditions (states)
class Time: pass # hit-the-time-limit state
class Size: pass # hit-the-size-limit state
class End: pass # hit-the-end state

class AWrapper(object):
	'''Async I/O objects' wrapper'''

	bs_default = 8192
	bs_max = 65536

	def __init__(self, pipe):
		if isinstance(pipe, int):
			fd = self._fd = pipe
			pipe = os.fromfd(pipe)
		else: fd = self._fd = pipe.fileno()
		self._poll_in, self._poll_out = epoll(), epoll()
		self._poll_in.register(fd, EPOLLIN | EPOLLERR | EPOLLHUP)
		self._poll_out.register(fd, EPOLLOUT | EPOLLERR | EPOLLHUP)
		self.close = pipe.close
		self.reads = pipe.read
		self.writes = pipe.write

	def __del__(self):
		self._poll_in.close()
		self._poll_out.close()
		self.close()

	def read(self, bs=-1, to=-1, state=False): # read until timeout
		if to < 0: # use regular sync I/O
			buff = self.reads(bs)
			if state: return (buff, Size) if len(buff) == bs else (buff, End) # "Size" might mean "Size | End" here
			else: return buff
		try:
			flags = fcntl.fcntl(self._fd, fcntl.F_GETFL)
			fcntl.fcntl(self._fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)
			deadline = time() + to
			buff = buffer('')
			while bs:
				try: fd, event = self._poll_in.poll(to, 1)[0] # get first event, fd should be eq self._fd
				except IndexError:
					if state: state = Time
					break
				if event != EPOLLHUP: # some data or error present
					ext = self.reads(min(bs, self.bs_max) if bs > 0 else self.bs_default) # min() for G+ reads
					buff += ext
				if event & EPOLLHUP: # socket is closed on the other end
					if state: state = End
					break
				to = deadline - time()
				if to < 0:
					if state: state = Time
					break
				bs -= len(ext)
			else: state = Size # got bs bytes
		finally:
			try: fcntl.fcntl(self._fd, fcntl.F_SETFL, flags) # restore blocking state
			except: pass # in case there was an error, caused by wrong fd/pipe (not to raise another one)
		return buff if not state else (buff, state)

	def write(self, buff, to=-1, state=False): # mostly similar (in reverse) to read
		if to < 0:
			bs = self.writes(buff)
			if state: return (bs, Size) if len(buff) == bs else (bs, End) # "Size" might mean "Size | End" here
			else: return bs
		try:
			flags = fcntl.fcntl(self._fd, fcntl.F_GETFL)
			fcntl.fcntl(self._fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)
			bs = 0
			deadline = time() + to
			while buff:
				try: fd, event = self._poll_out.poll(to, 1)[0]
				except IndexError:
					if state: state = Time
					break
				if event != EPOLLHUP:
					ext = os.write(fd, buff)
					bs += ext
				if event & EPOLLHUP:
					if state: state = End
					break
				to = deadline - time()
				if to < 0:
					if state: state = Time
					break
				buff = buffer(buff, ext)
		finally:
			try: fcntl.fcntl(self._fd, fcntl.F_SETFL, flags)
			except: pass
		return bs if not state else (bs, state)



import signal

class AExec(Popen):
	def __init__(self, *argz, **kwz): # keywords aren't used yet
		if len(argz) == 1: argz = (argz[0],) if isinstance(argz[0], (str, unicode, buffer)) else argz[0]
		try: sync = kwz.pop('sync')
		except KeyError: sync = True
		super(AExec, self).__init__(argz, **kwz)
		if self.stdin:
			if not sync: self.stdin = AWrapper(self.stdin)
			self.write = self.stdin.write
		if self.stdout:
			if not sync: self.stdout = AWrapper(self.stdout)
			self.read = self.stdout.read
		if self.stderr:
			if not sync: self.stderr = AWrapper(self.stderr)
			self.read_err = self.stderr.read

	def wait(self, to=-1):
		if to > 0:
			ts, fuse, action = time(), signal.alarm(to), signal.getsignal(signal.SIGALRM)
			def quit(s,f): raise StopIteration
			signal.signal(signal.SIGALRM, quit)
			try: status = super(AExec, self).wait()
			except StopIteration: return Time
			signal.signal(signal.SIGALRM, action)
			if fuse:
				fuse = int(time() - ts + fuse)
				if fuse > 0: signal.alarm(fuse)
				else: # trigger it immediately
					signal.alarm(0)
					os.kill(os.getpid(), signal.SIGALRM)
			else: signal.alarm(0)
		else: status = super(AExec, self).wait()
		return status

	def close(self, to=-1, to_sever=3):
		try:
			if self.stdin: # try to strangle it
				try: self.stdin.close()
				except: pass
				if to_sever and to > to_sever: # wait for process to die on it's own
					status = self.wait(to_sever)
					if not status is Time: return status
					else: to -= to_sever
			self.terminate() # soft-kill
			status = self.wait(to)
			if status is Time:
				self.kill() # hard-kill
				return Time
		except: return None # already taken care of
	__del__ = close
