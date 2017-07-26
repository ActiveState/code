###Embed lyrics into MP3 files using mutagen (USLT tag), optionally set other ID3 tags

Originally published: 2010-03-23 10:17:21
Last updated: 2011-05-17 15:56:56
Author: ccpizza 

Quick and dirty script to embed unsynchronized lyrics or any other text into MP3 files. The text files with the lyrics are expected to be in the same folder: i.e. for MySong.mp3 the lyrics text should be in the file MySong.txt.\n\nThe encoding of the text file will be probed in the following order: 'utf8','iso-8859-1','iso-8859-15','cp1252','cp1251','latin1'. If you need support for more encodings, a list is available at http://docs.python.org/release/2.5.2/lib/standard-encodings.html\n\nTo see the lyrics on an iPod (tested on 6G Classic) you need to press the middle button four times while a song is playing.\n\nThe script can also be used to set other ID3 tags. By default SET_OTHER_ID3_TAGS is False so existing ID3 tags will NOT be overwritten.\n\n\nUsage:\nRunning the file without arguments will process all MP3 files in the current directory.\n\nAlternatively the path to the folder with MP3's can be passed as the first argument.\n