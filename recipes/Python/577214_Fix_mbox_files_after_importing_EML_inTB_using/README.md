## Fix mbox files after importing EML into TB using ImportExportTools  
Originally published: 2010-05-02 13:20:15  
Last updated: 2010-05-02 13:21:00  
Author: Denis Barmenkov  
  
I've found a bug in import EML file into Thunderbird using ImportExportTools addon:
when I import eml file into TB there are a 'From' line added to mbox followed with EML file contents.
TB maintains right 'From' line for messages fetched from mailservers:

    From - Tue Apr 27 19:42:22 2010

ImportExportTools formats this line wrong I suppose that used some system function with default specifier so I saw in mbox file:

    From - Sat May 01 2010 15:07:31 GMT+0400 (Russian Daylight Time)

So there are two errors:
1) sequence 'time year' broken into 'year time'
2) extra trash with GMT info along with time zone name

This prevents the mbox file parsing using Python standard library (for sample) because there are a hardcoded regexp for matching From line (file lib/mailbox.py, class UnixMailbox):

    _fromlinepattern = r"From \s*[^\s]+\s+\w\w\w\s+\w\w\w\s+\d?\d\s+" \
                       r"\d?\d:\d\d(:\d\d)?(\s+[^\s]+)?\s+\d\d\d\d\s*$" 

Attached script fixes incorrect From lines so parsing those mboxes using Python standard library will become ok.