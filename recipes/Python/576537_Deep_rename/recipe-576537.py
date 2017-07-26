#!/usr/bin/python

# NOTE: This script has only been tested on Linux. In order to get it to work
# on Windows or Mac OS, find a working implementation of getchar/getch and
# replace the function getch below.

import os
import os.path
import re
import getopt
import sys, tty, termios

# Prevent infinite recursion in case of mistake
ITERATION_LIMIT = 100

FILENAME_ENDINGS = ['.py','.js','.html']

INTERACTIVE = False
MAKE_BACKUPS = False
DRY_RUN = False
TOP = os.getcwd()

USAGE = """Usage: deeprename [-i] [-b] oldword newword

Replace all occurrences of oldword with newword in all source files
(javascript, python, html) throughout the entire directory tree rooted at the
current working directory. Hidden files and directories are skipped.

-i: interactive mode
-b: make backups
-l: do not rename, just print out files that will be checked and exit
-d: dry run: just show files and lines that will be changed, don't make any changes

"""
### Getch

def getch(echo = False):
  fd = sys.stdin.fileno()
  old_settings = termios.tcgetattr(fd)
  try:
      tty.setraw(sys.stdin.fileno())
      ch = sys.stdin.read(1)
  finally:
      termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
  if echo: sys.stdout.write(ch)
  return ch

def gen_filepaths():
  return (pth for pth in all_filepaths() if pth.find('/.') == -1 and any(pth.endswith(ending) for ending in FILENAME_ENDINGS))

def all_filepaths():
  for path, dirlist, filelist in os.walk(TOP):
    for filename in filelist:
      yield os.path.join(path, filename)

def replaced_line(pat,sub,original_line):
  if DRY_RUN: return original_line
  line = original_line
  n = 0
  while True:
    if n > ITERATION_LIMIT:
      raise Exception("iteration limit exceeded on line: \n%s" % original_line)
    n += 1
    if pat.search(line):
      line = re.sub(pat,sub,line)
    else:
      return line

def file_has_pattern(pat,filepath):
  f = open(filepath)
  for line in f:
    if pat.search(line):
      f.close()
      return True
  f.close()
  return False

def prompt_line(pat,line):
  line = line.rstrip()
  matchobj = pat.search(line)
  start, end = matchobj.start(), matchobj.end()
  start = max(0,start - 25)
  prompt_line = line[start:end + 25]
  prompt_line = prompt_line[:60]
  prompt_line = prompt_line + (60 - len(prompt_line)) * ' '
  if start > 0:
    prompt_line = '...' + prompt_line[3:]
  return prompt_line

def user_prompt(pat,line):
  sys.stdout.write(prompt_line(pat,line) + ": ")
  return_value = getch(True)
  sys.stdout.write('\n')
  return return_value

def deeprename_files(pat,sub):
  for filepath in gen_filepaths():
    if file_has_pattern(pat,filepath):
      print "========================================"
      print "== %s" % filepath
      print "========================================"
      filepath_bak = filepath + '.bak'
      os.rename(filepath, filepath_bak)
      f = open(filepath_bak)
      g = open(filepath,"w")
      if INTERACTIVE:
        continue_rename = rename_one_interactive(f,g,pat,sub)
        if not continue_rename:
          break
      else:
        rename_one(f,g,pat,sub)
      if not MAKE_BACKUPS:
        os.remove(filepath_bak)
  
def rename_one_interactive(f,g,pat,sub):
  f = iter(f)
  while True:
    try:
      line = f.next()
    except StopIteration:
      return True
    if not pat.search(line):
      g.write(line)
    else:
      user_cmd = user_prompt(pat,line)
      if user_cmd == 'y':
        # replace the line and continue
        g.write(replaced_line(pat,sub,line))
      elif user_cmd == 'n':
        # use original line
        g.write(line)
      elif user_cmd == 'q':
        # quit
        g.write(line)
        # flush remaining lines
        for line in f:
          if pat.search(line): print prompt_line(pat,line)
          g.write(line)
        return False

def rename_one(f,g,pat,sub):
  for line in f:
    if pat.search(line):
      print prompt_line(pat,line)
      g.write(replaced_line(pat,sub,line))
    else:
      g.write(line)

def check_bakfiles():
  bakpaths = [pth for pth in all_filepaths() if pth.endswith('.bak')]
  if len(bakpaths) > 0:
    raise Exception("Fatal: backup files ('.bak') detected: %s" % ', '.join(bakpaths))
    
def check_swapfiles():
  swappaths = [pth for pth in all_filepaths() if pth.endswith('.swp')]
  if len(swappaths) > 0:
    raise Exception("Fatal: editor swap files ('.swp') detected: %s" % ', '.join(swappaths))

def exec_cmd():
  global INTERACTIVE, MAKE_BACKUPS, DRY_RUN
  oplist,args = getopt.getopt(sys.argv[1:],"ibldh")
  check_bakfiles()
  check_swapfiles()
  for opt, val in oplist:
    if opt == '-h':
      print USAGE
      return None
    if opt == '-i':
      INTERACTIVE = True
    elif opt == '-b':
      MAKE_BACKUPS = True
    elif opt == '-d':
      DRY_RUN = True
    elif opt == '-l':
      for filename in gen_filepaths():
        print filename
      return None
  if len(args) != 2:
    print USAGE
    return None
  name, sub = args
  deeprename_files(re.compile(r"\b" + name + r"\b"), sub)

if __name__ == '__main__':
  exec_cmd()
