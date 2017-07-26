#!/usr/bin/python2.5
# -*- coding: utf-8 -*-
"""Diff two directories of Word documents, providing extra context as well, using antiword and dwdiff."""
# (c) Copyright 2010 by Joseph Reagle
# Licensed under the GPLv3, see <http://www.gnu.org/licenses/gpl-3.0.html>
#

from glob import glob
from os import chdir, mkdir, rename
from os.path import exists, splitext
import re
from shutil import move, rmtree
from subprocess import call, Popen, PIPE
import sys


def create_txts(path):
    path_txt = path + 'text/'
    if exists(path_txt):
        rmtree(path_txt)
    mkdir(path_txt)
    chdir(path)
    for src_fn in glob('*.doc'):
        fn, ext = splitext(src_fn)
        call(['/usr/bin/antiword', '-w0', src_fn],
            stdout=file('text/' + fn + '.txt', 'w'))


pair_diff = r"""[^# ]+\s*(?:#[-].*?[\+]#|[^#]\s+#[\+].*?[-]#)\s*[^# ]+"""
single_diff = r"""[^# ]+\s*(?:#[\+][^#]+[\+]#|#[-][^#]+[-]#)\s*[^# ]+"""
diff_re = re.compile('(' + pair_diff + '|' + single_diff + ')')
footnote_re = re.compile('\d+\)?\+\]')

def create_diffs(old, new):
    # dwdiff ~/_joseph/2010/faith/latex-fai/doc/text/reagle_01.txt ~/_joseph/2010/faith-composition/text/reagle_01.txt
    old_path = old + 'text/'
    new_path = new + 'text/'
    chdir(new_path)
    for src_fn in sorted(glob('*.txt')):
        fn, ext = splitext(src_fn)
        f_out = file(fn + '.diff', 'w')
        print '\n' + src_fn
        output = Popen(['dwdiff', '-w', '#-', '-x', '-#', '-y', '#+', '-z' '+#',
			old_path + src_fn, new_path + src_fn], stdout=PIPE) # use # for easier parsing
        content = output.communicate()[0]
        if content:
            for line in content.split('\n'):
				if '{Notes begin}' in line:
					break
				match_obj = diff_re.findall(line)
				if match_obj:
					f_out.write('\n')
					for match in match_obj:
						# replace more readable symbols
						match = match.replace('#-', '{-') \
							.replace('-#', '-}') \
							.replace('#+', '[+') \
							.replace('+#', '+]')
						if not (footnote_re.search(match) or '—' in match or
							'–' in match):
							f_out.write(match + '\n')
        f_out.close()

if '__main__' == __name__:

    MY_SRC = '/home/reagle/_joseph/a'
    MIT_SRC = '/home/reagle/_joseph/b' # the version sent to compositers.
    create_txts(MY_SRC)
    create_txts(MIT_SRC)
    create_diffs(MY_SRC, MIT_SRC)
