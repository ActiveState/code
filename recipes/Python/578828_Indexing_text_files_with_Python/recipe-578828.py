"""
text_file_indexer.py
A program to index a text file.
Author: Vasudev Ram - www.dancingbison.com
Copyright 2014 Vasudev Ram
Given a text file somefile.txt, the program will read it completely, 
and while doing so, record the occurrences of each unique word, 
and the line numbers on which they occur. This information is 
then written to an index file somefile.idx, which is also a text 
file.
"""

import sys
import os
import string
from debug1 import debug1

def index_text_file(txt_filename, idx_filename, 
    delimiter_chars=",.;:!?"):
    """
    Function to read txt_file name and create an index of the 
    occurrences of words in it. The index is written to idx_filename.
    There is one index entry per line in the index file. An index entry 
    is of the form: word line_num line_num line_num ...
    where "word" is a word occurring in the text file, and the instances 
    of "line_num" are the line numbers on which that word occurs in the 
    text file. The lines in the index file are sorted by the leading word 
    on the line. The line numbers in an index entry are sorted in 
    ascending order. The argument delimiter_chars is a string of one or 
    more characters that may adjoin words and the input and are not 
    wanted to be considered as part of the word. The function will remove 
    those delimiter characters from the edges of the words before the rest 
    of the processing.
    """
    try:
        txt_fil = open(txt_filename, "r")
        """
        Dictionary to hold words and the line numbers on which 
        they occur. Each key in the dictionary is a word and the 
        value corresponding to that key is a list of line numbers 
        on which that word occurs in txt_filename.
        """

        word_occurrences = {}
        line_num = 0

        for lin in txt_fil:
            line_num += 1
            debug1("line_num", line_num)
            # Split the line into words delimited by whitespace.
            words = lin.split()
            debug1("words", words)
            # Remove unwanted delimiter characters adjoining words.
            words2 = [ word.strip(delimiter_chars) for word in words ]
            debug1("words2", words2)
            # Find and save the occurrences of each word in the line.
            for word in words2:
                if word_occurrences.has_key(word):
                    word_occurrences[word].append(line_num)
                else:
                    word_occurrences[word] = [ line_num ]

        debug1("Processed {} lines".format(line_num))

        if line_num < 1:
            print "No lines found in text file, no index file created."
            txt_fil.close()
            sys.exit(0)

        # Display results.
        word_keys = word_occurrences.keys()
        print "{} unique words found.".format(len(word_keys))
        debug1("Word_occurrences", word_occurrences)
        word_keys = word_occurrences.keys()
        debug1("word_keys", word_keys)

        # Sort the words in the word_keys list.
        word_keys.sort()
        debug1("after sort, word_keys", word_keys)

        # Create the index file.
        idx_fil = open(idx_filename, "w")

        # Write the words and their line numbers to the index file.
        # Since we read the text file sequentially, there is no need 
        # to sort the line numbers associated with each word; they are 
        # already in sorted order.
        for word in word_keys:
            line_nums = word_occurrences[word]
            idx_fil.write(word + " ")
            for line_num in line_nums:
                idx_fil.write(str(line_num) + " ")
            idx_fil.write("\n")

        txt_fil.close()
        idx_fil.close()
    except IOError as ioe:
        sys.stderr.write("Caught IOError: " + repr(ioe) + "\n")
        sys.exit(1)
    except Exception as e:
        sys.stderr.write("Caught Exception: " + repr(e) + "\n")
        sys.exit(1)

def usage(sys_argv):
    sys.stderr.write("Usage: {} text_file.txt index_file.txt\n".format(
        sys_argv[0]))

def main():
    if len(sys.argv) != 3:
        usage(sys.argv)
        sys.exit(1)
    index_text_file(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
    main()

# EOF
