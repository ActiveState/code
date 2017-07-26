## Line-oriented processing in Python from command line (like AWK)  
Originally published: 2011-04-14 19:48:15  
Last updated: 2011-04-14 19:49:16  
Author: Artur Siekielski  
  
A very simple but powerful shell script which enables writing ad-hoc Python scripts for processing line-oriented input. It executes the following code template:

    $INIT
    for line in sys.stdin:
        $LOOP
    $END

where $INIT, $LOOP and $END code blocks are given from command line. If only one argument is given, then $INIT and $END are empty. If two arguments are given, $END is empty.

Examples (script is saved as 'pyk' in the $PATH):

* "wc -l" replacement:
    $ cat file | pyk 'c=0' 'c+=1' 'print c'
* grep replacement:
    $ cat file | pyk 'import re' 'if re.search("\d+", line): print line'
* adding all numbers:
    $ seq 1 10 | pyk 's=0' 's+=int(line)' 'print s'
* prepending lines with it's length:
    $ cat file | pyk 'print len(line), line'
* longest file name:
    $ ls -1 | pyk 'longest=""' 'if len(line) > len(longest): longest=line' 'print longest'
* number of unique words in a document:
    $ pyk 'words=[]' 'words.extend(line.split())' 'print "All words: {}, unique: {}".format(len(words), len(set(words))'
