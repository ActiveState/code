'''urlnorm.py
(c) 1999 Mark Nottingham <mnot@pobox.com>

Routines to normalise a URL.

* lowercases the scheme and hostname
* takes out default port if present (e.g., http://www.foo.com:80/)
* collapses the path (./, ../, etc)
* removes the last character in the hostname if it is '.'
* unquotes any %-escaped characters

available functions:

norms - given a URL (string), returns a normalised URL
norm - given a URL tuple, returns a normalised tuple
test - test suite
'''

# THIS SOFTWARE IS PROVIDED "AS IS", WITH NO WARRANTY OF ANY KIND
# some stuff stolen from RFC 1808.

from urlparse import urlparse, urlunparse
from urllib import unquote
from string import rfind, lower
import re


__version__ = "0.9"

_re_pat = re.compile('([^/]+/\.\./?|/\./|//|/\.$|/\.\.$)')


_default_port = {	'http': ':80',
					'https': ':443',
					'gopher': ':70',
					'news': ':119',
					'snews': ':563',
					'nntp': ':119',
					'snntp': ':563',
					'ftp': ':21',
					'telnet': ':23',
					'prospero': ':191',
				}

_relative_scheme = {	'http': 1,
						'https': 1,
						'news': 1,
						'snews': 1,
						'nntp': 1,
						'snntp': 1,
						'ftp': 1,
						'file': 1,
						'': 1
					}



def norms(urlstring=''):
	return urlunparse(norm(urlparse(urlstring)))


def norm(urltuple=('','','','','','')):
	(scheme, host, path, parameters, query, fragment) = urltuple
	scheme = lower(scheme)
	host = lower(host)
	
	if _relative_scheme.get(scheme, 0):
		last_path = path
		while 1:
			path = re.sub(_re_pat, '/', path, 1)
			if last_path == path:
				break
			last_path = path
			
	path = unquote(path)

	colon_idx = rfind(host, ':')
	if colon_idx > 0:
		if host[colon_idx:] == _default_port.get(scheme, '#'):
			host = host[:colon_idx]
		if host[colon_idx - 1] == '.':
			host = host[:colon_idx - 1] + host[colon_idx:]
	else:
		try:
			if host[-1] == '.':
				host = host[:-1]
		except IndexError:
			pass

	return (scheme, host, path, parameters, query, fragment)



def test():
	tests = {	'/foo/bar/.':				'/foo/bar/', 
			'/foo/bar/./':				'/foo/bar/',
			'/foo/bar/..':				'/foo/',
			'/foo/bar/../': 			'/foo/',
			'/foo/bar/../baz': 			'/foo/baz',
			'/foo/bar/../..': 			'/',
			'/foo/bar/../../': 			'/',
			'/foo/bar/../../baz': 		'/baz',
			'/foo/bar/../../../baz':	'/../baz',
			'/foo/bar/../../../../baz':	'/baz',
			'/./foo':				'/foo',
			'/../foo':			'/../foo',
			'/foo.':				'/foo.',
			'/.foo':				'/.foo',
			'/foo..':				'/foo..',
			'/..foo':				'/..foo',
			'/./../foo':				'/../foo',
			'/./foo/.':				'/foo/',
			'/foo/./bar':				'/foo/bar',
			'/foo/../bar':				'/bar',
			'/foo//':				'/foo/',
			'/foo///bar//':				'/foo/bar/',	
			'http://www.foo.com:80/foo':	'http://www.foo.com/foo',
			'http://www.foo.com:8000/foo':	'http://www.foo.com:8000/foo',
			'http://www.foo.com./foo/bar.html': 'http://www.foo.com/foo/bar.html',
			'http://www.foo.com.:81/foo':	'http://www.foo.com:81/foo',
			'http://www.foo.com/%7ebar':	'http://www.foo.com/~bar',
			'http://www.foo.com/%7Ebar':	'http://www.foo.com/~bar',
			'ftp://user:pass@ftp.foo.net/foo/bar': 'ftp://user:pass@ftp.foo.net/foo/bar',
				'-':						'-',
			}

	n_correct, n_fail = 0, 0
	test_keys = tests.keys()
	test_keys.sort()		
	
	for i in test_keys:
		print 'ORIGINAL:', i
		cleaned = norms(i)

		answer = tests[i]
		print 'CLEANED: ', cleaned
		print 'CORRECT: ', answer
		if cleaned != answer:
			print "*** TEST FAILED"
			n_fail = n_fail + 1
		else:
			n_correct = n_correct + 1
		print
		
	print "TOTAL CORRECT:", n_correct
	print "TOTAL FAILURE:", n_fail
