import sys
import re
import mechanize
import pullparser

SOURCEFORGE_URL = 'http://sourceforge.net/softwaremap/trove_list.php?form_cat=160'
# sourceforge.net, projects per programming language, parser tokens:
"""
Token('starttag', 'a', [('href', 'trove_list.php?form_cat=163')]),
Token('starttag', 'img', [('src', 'http://images.sourceforge.net..'), ...)
Token('entityref', 'nbsp', None),
Token('data', ' Ada', None),
Token('endtag', 'a', None),
Token('data', ' ', None)]
Token('starttag', 'i', []),
Token('data', '(100 projects)', None),
"""
FRESHMEAT_URL = 'http://freshmeat.net/browse/160/?topic_id=160'
# projects per programming language, parser tokens:
"""
Token('data', 'Programming Language', None),
Token('endtag', 'b', None),
Token('data', '\r\n              ', None),
Token('starttag', 'br', []),
Token('data', '\r\n      \n\r\n      ', None),
Token('starttag', 'li', []),
Token('starttag', 'a', [('href', '/browse/163/')]),
Token('starttag', 'b', []),
Token('data', 'Ada', None),
Token('endtag', 'b', None),
Token('endtag', 'a', None),
Token('data', '\r\n          ', None),
Token('starttag', 'small', []),
Token('data', '(57 projects)', None),
Token('endtag', 'small', None),
Token('data', '\r\n              ', None),
Token('starttag', 'li', []),
Token('starttag', 'a', [('href', '/browse/161/')]),
"""

def get_n_project(s):
	return int(re.compile(r'([\d]*) projects').findall(s)[0])
def sourceforge_get_language_statistics(parser):
	'sourceforge_get_language_statistics(file_obj) -> [ (n_project, language), ... ]'
	def is_language_link(token):
		try:
			if token.type == 'starttag' and token.data == 'a' \
				and 'trove_list.php?form_cat=' in token.attrs[0][1]:
					return True
		except IndexError:
			return False
		return False
	for t in parser.tags():
		if is_language_link(t):
			l = [
			(parser.next(), 'img'),
			(parser.next(), 'nbsp'),
			(parser.next(), 'data(language)'),
			(parser.next(), '/a'),
			(parser.next(), 'data'),
			(parser.next(), 'i'),
			(parser.next(), 'data(n_project)'), ]

			language = l[2][0].data.strip()
			n = l[6][0].data.strip()
			try:
				n_project = get_n_project(n)
			except IndexError:
				continue
			else:
				yield (n_project, language)

def freshmeat_get_language_statistics(parser):
	def is_language_link(token):
		try:
			if token.type == 'starttag' and token.data == 'a' \
				and '/browse/' in token.attrs[0][1]:
					return True
		except IndexError:
			return False
		return False
	for t in parser.tags():
		if is_language_link(t):
			l = [
			(parser.next(), 'b'),
			(parser.next(), 'data(language)'),
			(parser.next(), '/b'),
			(parser.next(), 'a'),
			(parser.next(), 'data'),
			(parser.next(), 'small'),
			(parser.next(), 'data(n_project)'), ]
			language = l[1][0].data.strip()
			n = l[6][0].data
			try:
				n_project = get_n_project(n)
			except IndexError:
				continue
			else:
				yield (n_project, language)

for (name, url, get_statistics) in (
		('sourceforge.net', SOURCEFORGE_URL,
			sourceforge_get_language_statistics),
		('freshmeat.net', FRESHMEAT_URL,
			freshmeat_get_language_statistics),):
	b = mechanize.Browser()
	b.set_handle_robots(False)
	b.open(url)
	r = b.response()
	r.seek(0)
	p = pullparser.PullParser(r)
	l = list(get_statistics(p))
	l.sort()
	l.reverse()
	print name
	for (n_project, language) in l:
		print '%6d %s' % (n_project, language)
	print
