# bentley_knuth.py
# Author: Vasudev Ram - http://www.dancingbison.com
# Version: 0.1

# The problem this program tries to solve is from the page:
# http://www.leancrew.com/all-this/2011/12/more-shell-less-egg/

# Description: The program Bentley asked Knuth to write:

# Read a file of text, determine the n most frequently 
# used words, and print out a sorted list of those words 
# along with their frequencies.

import sys
import os
import string

sys_argv = sys.argv

def usage():
 sys.stderr.write("Usage: %s n file\n" % sys_argv[0])
 sys.stderr.write("where n is the number of most frequently\n")
 sys.stderr.write("used words you want to find, and \n")
 sys.stderr.write("file is the name of the file in which to look.\n")

if len(sys_argv) < 3:
 usage()
 sys.exit(1)

try:
 n = int(sys_argv[1])
except ValueError:
 sys.stderr.write("%s: Error: %s is not a decimal numeric value" % (sys_argv[0], 
  sys_argv[1]))
 sys.exit(1)

print "n =", n
if n < 1:
 sys.stderr.write("%s: Error: %s is not a positive value" % 
  (sys_argv[0], sys_argv[1]))

in_filename = sys.argv[2]
print "%s: Finding %d most frequent words in file %s" % \
 (sys_argv[0], n, in_filename)

try:
 fil_in = open(in_filename)
except IOError:
 sys.stderr.write("%s: ERROR: Could not open in_filename %s\n" % \
  (sys_argv[0], in_filename))
 sys.exit(1)

word_freq_dict = {}

for lin in fil_in:
 words_in_line = lin.split()
 for word in words_in_line:
  if word_freq_dict.has_key(word):
   word_freq_dict[word] += 1
  else:
   word_freq_dict[word] = 1

word_freq_list = []
for item in word_freq_dict.items():
 word_freq_list.append(item)

wfl = sorted(word_freq_list, 
 key=lambda word_freq_list: word_freq_list[1], reverse=True)
#wfl.reverse()
print "The %d most frequent words sorted by decreasing frequency:" % n
len_wfl = len(wfl)
if n > len_wfl:
 print "n = %d, file has only %d unique words," % (n, len_wfl)
 print "so printing %d words" % len_wfl
print "Word: Frequency"
m = min(n, len_wfl)
for i in range(m):
 print wfl[i][0], ": ", wfl[i][1]

fil_in.close()
