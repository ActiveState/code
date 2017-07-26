#!/usr/bin/python

import os
import os.path
import sys
import md5
from stat import *
from optparse import OptionParser

class Stats:
	def __init__(self):
		self.filenb = 0
		self.dirnb = 0
		self.othernb = 0
		self.unstatablenb = 0

def scan_tree(lst, maxlen, dirname, dirpath, prefix, nxt_prefix, options, stats):
	"""params:
	 lst: I/O list of (tree_ascii_art_repr_line, path_if_regular_file_else_None)
	  where both are strings and the second one can also be None
	 maxlen: integer that contains the rightmost column number of ascii repr of
	  the tree known by the caller
	 dirname: name of the directory from which a tree repr is wanted
	 dirpath: path to the directory from which a tree repr is wanted
	 prefix: string to prepend to the dirname to form the first line of the ascii
	  repr of the subtree
	 nxt_prefix: string to prepend to every lines of the repr of the subtree but
	  the first one (which uses prefix)
	 options: options as extracted by the optparse module from cmd line options
	 stats: Stats instance
	returns a new value for maxlen
	"""
	try:
		dir_content = os.listdir(dirpath)
		dir_content.sort()
	except OSError:
		dir_content = None
	ascii_art_tree_repr = prefix + dirname
	maxlen = max(maxlen, len(ascii_art_tree_repr))
	if dir_content is None:
		lst.append((ascii_art_tree_repr + ' [error reading dir]', None))
		return maxlen
	if not options.all:
		dir_content = [child for child in dir_content if child[0] != '.']
	lst.append((ascii_art_tree_repr, None))
	sub_prefix     = nxt_prefix + '|-- '
	sub_nxt_prefix = nxt_prefix + '|   '
	for num, child in enumerate(dir_content):
		if num == len(dir_content) - 1:
			sub_prefix     = nxt_prefix + '`-- '
			sub_nxt_prefix = nxt_prefix + '    '
		joined_path = os.path.join(dirpath, child)
		try:
			lmode = os.lstat(joined_path)[ST_MODE]
		except:
			lmode = None
		ascii_art_tree_repr = sub_prefix + child
		maxlen = max(maxlen, len(ascii_art_tree_repr))
		if lmode is None:
			stats.unstatablenb += 1
			lst.append((ascii_art_tree_repr + ' [error stating child]', None))
		elif S_ISREG(lmode):
			stats.filenb += 1
			lst.append((ascii_art_tree_repr, joined_path))
		elif S_ISDIR(lmode):
			stats.dirnb += 1
			maxlen = scan_tree(lst, maxlen, child, joined_path, sub_prefix, sub_nxt_prefix, options, stats)
		elif S_ISLNK(lmode):
			stats.filenb += 1
			try:
				lst.append((ascii_art_tree_repr + ' -> ' + os.readlink(joined_path), None))
			except OSError:
				lst.append((ascii_art_tree_repr + ' [cannot read symlink]', None))
		elif S_ISCHR(lmode):
			stats.othernb += 1
			lst.append((ascii_art_tree_repr + ' [char device]', None))
		elif S_ISBLK(lmode):
			stats.othernb += 1
			lst.append((ascii_art_tree_repr + ' [block device]', None))
		elif S_ISFIFO(lmode):
			stats.othernb += 1
			lst.append((ascii_art_tree_repr + ' [fifo]', None))
		elif S_ISSOCK(lmode):
			stats.othernb += 1
			lst.append((ascii_art_tree_repr + ' [socket]', None))
		else:
			stats.othernb += 1
			lst.append((ascii_art_tree_repr + ' [unknown]', None))
	return maxlen		

def md5_from_path(path):
	"""Returns an hex repr of the md5sum of the file content path points to.
	On IOError returns '<unable to read file>'.
	"""
	try:
		f = open(path)
		m = md5.new()
		while True:
			b = f.read(262144)
			if not b:
				break
			m.update(b)
		f.close()
		return m.hexdigest()
	except IOError:
		return '<unable to read file>'

def main():
	parser = OptionParser(usage="usage: %prog [options] [dir1 [dir2 [...]]]")
	parser.add_option("-a", "--all", action='store_true', dest='all', default=False, help="All files are listed.")
	options, roots = parser.parse_args()
	stats = Stats()
	if not roots:
		roots = ['.']
	for root in roots:
		lst = []
		maxlen = scan_tree(lst, 0, root, root, "", "", options, stats)
		for line, path in lst:
			if path is not None:
				m = md5_from_path(path)
				print line + ' ' * (maxlen+1-len(line)) + m
			else:
				print line
	print
	print ', '.join((
		('%d directory', '%d directories')[stats.dirnb > 1] % stats.dirnb,
		('%d file', '%d files')[stats.filenb > 1] % stats.filenb,
		('%d other', '%d others')[stats.othernb > 1] % stats.othernb,
		('%d unstatable', '%d unstatables')[stats.unstatablenb > 1] % stats.unstatablenb))

if __name__ == "__main__":
	main()
