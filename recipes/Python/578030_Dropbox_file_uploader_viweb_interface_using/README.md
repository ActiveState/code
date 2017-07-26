## Dropbox file uploader via web interface using Python with urllib2 and mechanize  
Originally published: 2012-02-01 17:31:16  
Last updated: 2016-04-28 13:21:43  
Author: ccpizza   
  
UPDATE:
This is script is not maintained and does not anymore with the current version of Dropbox. For a proper command line interface to dropbox I recommend `dropbox_uploader`: https://github.com/andreafabrizi/Dropbox-Uploader

Originally inspired by the example at http://joncraton.org/blog/62/uploading-dropbox-python. 

The script uses mechanize to logon to the web page and upload the file(s) to the Dropbox root folder or to the folder supplied on the command line as `dir:/my_dropbox_path` (if present, this must be the first parameter).

Multiple files and/or glob patterns names are accepted as script arguments.

Example usage
--------------

    dropbox.py file1.txt                       # upload to root folder
    dropbox.py dir:/Backups/2012 file1.txt     # upload to custom folder
    dropbox.py dir:/Backups/2012 *.txt         # upload by file mask
    dropbox.py dir:/Backups/2020 *             # upload all files in current dir

Limitations: only files in current folder are processed, subfolders are ignored.

NOTE
----

The script requires the `mechanize` module - use `pip install mechanize` or `easy_install mechanize` to add it to your site-packages.

NOTE2
------
I have found a cleaner way to manage dropbox files from the console - see the *dropbox-uploade*r script at https://github.com/andreafabrizi/Dropbox-Uploader - it is a Bash script that works using the official Dropbox API rather than emulating a web browser.