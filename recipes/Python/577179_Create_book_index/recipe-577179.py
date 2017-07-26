#!/usr/bin/python2.6
# -*- coding: utf-8 -*-
""" Read page indices to build book index. """
# index should be between 3 and 9 pages
#1. fix tricky names (e.g., van Rossum, Van Doren)

import codecs
import getopt
from optparse import OptionParser
import os
import re
import sys


ABBRV = (
		('NPOV', 'Neutral Point of View (NPOV)'),
		('IETF', 'Internet Engineering Task Force (IETF)'),
		('ODF', 'Open Document Format (ODF)'),
		('W3C', 'World Wide Web Consortium (W3C)'),
		('OASIS', 'Organization for the Advancement of Structured Information Standards'),
		)

BORING_WORDS = ('', 'a', 'also', 'of', 'if', 'in', 'an', 'to', 'for', 'the', 'and', 're')

NAMES = set() # from http://names.mongabay.com/
for line in open('/home/reagle/joseph/2010/03/names-male.csv'):
	NAMES.add(line.split(' ')[0])
for line in open('/home/reagle/joseph/2010/03/names-female.csv'):
	NAMES.add(line.split(' ')[0])
NAMES_EXCEPTIONS = set(['LONG'])
NAMES.difference_update(NAMES_EXCEPTIONS) # exceptions to the lists

KEEP_LOWER = ('danah', 'boyd')


def a_name(text):
	"""Test if a common first name.
	>>> a_name("John")
	True
	"""
	text = text.upper()
	if text[1] == '.': # e.g., H. G. Wells
		return True
	if text in NAMES:
		return True
	return False

def strip_var(v):
	"""Strip a bit of text
	>>> strip_var(' foo bar  ')
	'foo bar'
	"""
	if v:
		return v.strip()
	else:
		return None

def build_index(text):

	index = {}
	pattern_re = re.compile(
		r'(?P<topic>\D.+?) (?:see (?P<see_ref>.*)|(?P<pages>[0-9,\-n]+(?!\.)) ?(?P<subtopic>.*))')

	for line in text:
		if line == '':
			continue
		if opts.debug:
			print 'line =', line
		topic, see_ref, pages, subtopic = pattern_re.match(line).groupdict().values()
		topic, see_ref, pages, subtopic = map(strip_var, (topic, see_ref, pages, subtopic))
		chunks = topic.split(' ')
		if len(chunks) > 1:
			if a_name(chunks[0]):
				pre, last = topic.split(' ', 1)
				topic = chunks[-1] + ', ' + ' '.join(chunks[0:-1])
		if topic not in index:
			index[topic] = {}
		if see_ref:
			if see_ref.startswith('also '):
				index[topic].setdefault('also', []).append(see_ref[5:])
			else:
				index[topic].setdefault('see', []).append(see_ref)
		elif subtopic:
			index[topic].setdefault('subtopics', {}).setdefault(subtopic, []).append(pages)
		else:
			index[topic].setdefault('pages', []).append(pages)
	return index

def entitle(s):
	'''title case first word of refs
	>>> entitle('also monographic principle')
	'also monographic principle'
	>>> entitle('monographic principle')
	'Monographic principle'
	'''
	new_refs = []

	if s.startswith('\tsee also '): # remove 'see' prefix text
		s = s[10:]
		prefix = '. *See also* '
	elif s.startswith('\tsee '):
		s = s[5:]
		prefix = '. *See* '
	else:
		prefix = ''

	refs = s.split('; ')
	for ref in refs: # check refs
		words = ref.split()
		if words[0] not in BORING_WORDS and words[0][0].islower():
			words[0] = words[0].title()
		words = ' '.join(words)
		new_refs.append(words)
	return prefix + '; '.join(sorted(new_refs))


range_re = re.compile(u'\d+[-–n]\d+')
def sort_range(text):
	"""Sort index page refs such that:
	>>> sort_range('12-13')
	12
	>>> sort_range('5n3')
	5
	>>> sort_range('see also Smith')
	'see also Smith'

	"""
	if  range_re.match(text):
		if 'n' in text:
			text = text.split('n')[0]
		if '-' in text:
			text = text.split('-')[0]
		if u'–' in text:				# ndash
			text = text.split(u'–')[0]
	if text.isdigit():
		text = int(text)
	return text

def sort_topic(topic):
	topic = topic.replace('"', '').replace('*', '')
	words = topic.split(' ')
	if words[0] in ('and', 'on', 'see', 'also'):
		words.pop(0)
	words[0] = words[0].upper()
	return words

emphasis_re = re.compile(r'\*(.*)\*')
def fixup(s):
	"""Make some final formatting tweaks
	>>> fixup('on "zeal in research", 156')
	'on "zeal in research," 156'

	"""
	s = emphasis_re.sub(r'<em>\1</em>', s) # replace asterisks with balanced <em>
	return s.replace('",', ',"') # move comma inside quotes

def print_index(index):
	"""Print the index"""

	fdo.write('<html>'
		'<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>'
		'<body><pre>')
	for topic in sorted(index, key=sort_topic):
		topic_txt = topic
		pages_txt = see_txt = also_txt = ''

		# uppercase first letter of entries, and replace abbreviations
		if topic.split(', ')[0] not in KEEP_LOWER:
			topic_txt = topic[0].upper() + topic[1:]
		for abbrv, expansion in ABBRV:
			topic_txt = topic_txt.replace(abbrv, expansion)

		if 'pages' in index[topic]:
			pages_txt = ', ' + ', '.join(index[topic]['pages'])\
				.replace('-', u'–') # ndash

		# cross references
		if 'see' in index[topic] and index[topic]['see'] != [None]:
			see_refs = index[topic]['see']
			see_refs = [entitle(ref) for ref in see_refs]
			see_txt = '. *See* ' + '; '.join(sorted(see_refs))
		if 'also' in index[topic] and index[topic]['also'] != [None]:
			also_refs = index[topic]['also']
			also_refs = [entitle(ref) for ref in also_refs]
			also_txt = '. *See also* ' + '; '.join(sorted(also_refs))

		if 'subtopics' not in index[topic]:
			fdo.write(fixup(topic_txt + pages_txt + see_txt + also_txt + '\n'))
		else:
			subtopics = index[topic]['subtopics'] # a dict
			sub_txt = sub_pages_txt = ''
			sub_pages = []

			# join if topic has no pages itself and only one subtopic
			if 'pages' not in index[topic] and len(subtopics) == 1:
				sub_txt, sub_pages = subtopics.items()[0]
				sub_pages_txt = ', ' + ', '.join(sub_pages)\
					.replace('-', u'–') # ndash
				fdo.write(fixup(topic_txt + ', ' + sub_txt + sub_pages_txt + '\n'))
				continue

			# collapse if number of subentries below threshold
			elif 0 < len(subtopics) <= opts.collapse:
				for subtopic in subtopics:
					sub_pages.extend(subtopics[subtopic])
				sub_pages_txt += ', ' + ', '.join(sorted(sub_pages, key=sort_range))\
					.replace('-', u'–') # ndash
				fdo.write(fixup(topic_txt + sub_pages_txt + '\n'))
				continue

			# write out subtopics normally
			else:
				fdo.write(fixup(topic_txt + pages_txt + see_txt + also_txt + '\n'))
				for subtopic in subtopics:
					fdo.write(fixup('\t' + subtopic + ', '
						+ ', '.join(subtopics[subtopic]).replace('-', u'–') +'\n'))
	fdo.write('</pre></body></html>')



if __name__ == "__main__":
	sys.stdout = codecs.getwriter('UTF-8')(sys.__stdout__, errors='replace')

	parser = OptionParser(usage="usage: %prog [options] [FILE]")
	parser.add_option("-d", "--debug", default=False,
					action="store_true",
					help="print lines as processed")
	parser.add_option("-c", "--collapse", default=0,
					type="int",
					help="collapse if <= THRESHOLD subentries (default: %default)",
					metavar="THRESHOLD")
	parser.add_option("-t", "--tests",
					action="store_true", default=False,
					help="run tests")
	opts, files = parser.parse_args()

	if opts.tests:
		print "Running doctests"
		import doctest
		doctest.testmod()

	fn = files[0]
	fdi = codecs.open(fn, "rb", 'utf-8')
	text = [line.strip() for line in fdi.readlines()]
	text[0] = text[0].lstrip(unicode(codecs.BOM_UTF8, "utf8"))
	fileOut = os.path.splitext(fn)[0] + '-formatted.html'
	fdo = codecs.open(fileOut, "wb", "utf-8")

	index = build_index(text)
	print_index(index)
