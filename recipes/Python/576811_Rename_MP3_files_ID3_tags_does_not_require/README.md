## Rename MP3 files from ID3 tags (does not require external ID3 modules) 
Originally published: 2009-06-16 05:46:27 
Last updated: 2011-11-05 15:27:32 
Author: ccpizza  
 
Rename MP3 files in the current folder according to ID3 tags. This is based on Ned Batchelder's id3reader class. I only added the code in the `__main__` method.\n\n* When run without arguments, the script renames the files in the current folder. The directory can be specified explicitly as the first argument.\n* The files do not need to necessarily have the `MP3` extension.\n* To move the files to directories based on album name use the `-d` switch.\n* Does not work with other file types, such as OGG, M4A, MP4, etc.\n* This is a quick and dirty script that works for me most of the times. If you need more power, try mutagen, picard, mp3tag or something similar.