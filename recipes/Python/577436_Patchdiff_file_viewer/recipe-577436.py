#!/usr/bin/python3

# dv
#
# Highlights diff output (unified format):
# Usage: diff -u file1 file2 | dv
#        git diff | dv
#        cvs diff -u -D '1 year ago' -D '11 month ago' | dv
#
# Accepts input in system default encoding (usually utf8), conversion may be needed:
#        diff -u file1 file2 | iconv -f koi8-r | dv
#
# To install python3 and tkinter on ubuntu, run:
# sudo aptitude install python3-tk
#

import tkinter as tk
from tkinter import ttk
import difflib as dl
import sys
import itertools as it

FONT = ('Nimbus Mono L', 13)
FONT_B = ('Nimbus Mono L', 13, 'bold')

TAGS = {'diff' : {'font':FONT_B, 'foreground':'SkyBlue4'},

        'addition' : {'font':FONT_B, 'background':'LimeGreen', 'foreground':'yellow'},
        'removal' : {'font':FONT_B, 'background':'indian red', 'foreground':'yellow'},

        'removal-equal' : {'font':FONT_B, 'background':'gray80', 'foreground':'yellow'},
        'removal-insert' : {'font':FONT_B, 'background':'pink2', 'foreground':'yellow'},
        'removal-replace' : {'font':FONT_B, 'background':'pink3', 'foreground':'yellow'},
        'removal-delete' : {'font':FONT_B, 'background':'pink4', 'foreground':'yellow'},

        'addition-equal' : {'font':FONT_B, 'background':'gray82', 'foreground':'yellow'},
        'addition-insert' : {'font':FONT_B, 'background':'cyan2', 'foreground':'yellow'},
        'addition-replace' : {'font':FONT_B, 'background':'cyan3', 'foreground':'yellow'},
        'addition-delete' : {'font':FONT_B, 'background':'cyan4', 'foreground':'yellow'}}

tags = []

def getTextIndex(s, sLine, i):
  linesAdd = s.count("\n", 0, i)
  column = i - s.rfind("\n", 0, i) - 1
  return str(sLine + linesAdd) + '.' + str(column)

def addTag(s, sLine, i1, i2, name):
  tag = (name, getTextIndex(s, sLine, i1), getTextIndex(s, sLine, i2))
  tags.append(tag)

def compare(a, aLine, b, bLine):
  s = dl.SequenceMatcher(None, a, b)
  for tag, i1, i2, j1, j2 in s.get_opcodes():
    addTag(a, aLine, i1, i2, 'removal-' + tag);
    addTag(b, bLine, j1, j2, 'addition-' + tag);

diffText = ''
addition = ''
removal = ''
additionLine = 0
removalLine = 0
lineN = 0

for line in it.chain(sys.stdin, [' ']):
  lineN += 1
  if line.startswith('+') and not line.startswith('+++ '):
    addition += line[1:]
    if not additionLine:
      additionLine = lineN

  elif line.startswith('-') and not line.startswith('--- '):
    removal += line[1:]
    if not removalLine:
      removalLine = lineN

  else:

    if removal and addition:
      compare(removal, removalLine, addition, additionLine)
    elif removal:
      addTag(removal, removalLine, 0, len(removal), 'removal')
    elif addition:
      addTag(addition, additionLine, 0, len(addition), 'addition')

    if removal:
      diffText += removal
      removal = ''
      removalLine = 0

    if addition:
      diffText += addition
      addition = ''
      additionLine = 0

    if not line.startswith(' '):
      diffText += line
      addTag(line, lineN, 0, len(line)-1, 'diff')
    else:
      diffText += line[1:]

if diffText:
  root = tk.Tk()
  root.title('Diff Viewer: ' + str(lineN) + ' lines')

  text = tk.Text(root, width=100, height=40, font=FONT)
  text.grid(column=0, row=0, sticky='nsew')

  sb = ttk.Scrollbar(command=text.yview, orient='vertical')
  sb.grid(column=1, row=0, sticky='ns')
  text['yscrollcommand'] = sb.set

  root.columnconfigure(0, weight=1)
  root.rowconfigure(0, weight=1)

  text.insert('end', diffText)
  text['state'] = 'disabled'

  for t in tags:
    text.tag_add(*t)

  for t,v in TAGS.items():
    text.tag_config(t, **v)

  root.mainloop()
