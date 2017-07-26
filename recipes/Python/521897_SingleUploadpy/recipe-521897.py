# SingleUpload.py
from sys import stdin
from re import compile
from cgi import parse_header
from os import environ as env

search = compile(r'([^\\/]+)$').search

def open():
	global next, last
	try:
		next = '--' + parse_header(env['CONTENT_TYPE'])[1]['boundary']
	except:
		raise IOError

	last = next + '--'

	filename = None
	while not filename:
		while True:
			l = stdin.readline(65536)
			if not l:
				raise IOError

			if l[:2] == '--':
				sl = l.strip()
				if sl == next:
					break
				if sl == last:
					raise IOError

		for i in xrange(10):
			l = stdin.readline(65536).strip()
			if not l:
				break
			try:
				filename = parse_header(l.split(':', 1)[1])[1]['filename']
				break
			except:
				continue

	m = search(filename)
	if not m:
		raise IOError
	filename = m.groups()[0]

	while stdin.readline(65536).strip():
		pass

	def _readline():
		el = ''
		while True:
			l = stdin.readline(65536)
			if not l:
				raise IOError

			if l[:2] == '--' and el:
				sl = l.strip()
				if sl == next or sl == last:
					break

			ol, el = el, l[-2:] == '\r\n' and '\r\n' or (
				l[-1] == '\n' and '\n' or '')

			p = len(el)
			if p == 0:
				yield ol + l
			else:
				yield ol + l[:-p]
		while True:
			yield None

	rl = _readline().next
	def _next(size=65536):
		buff = _next.buff
		while len(buff) < size:
			l = rl()
			if not l:
				_next.buff = ''
				return buff

			buff += l

		r, _next.buff = buff[:size], buff[size:]
		return r

	_next.buff = rl()

	def _read(size=None):
		if size:
			return _next(size)

		fp = __import__('StringIO').StringIO()
		while True:
			l = _next()
			if not l:
				return fp.getvalue()

			fp.write(l)

	fp = type('SingleFile', (), {})()
	fp.next = _next; fp.read = _read
	fp.filename = filename

	return fp
