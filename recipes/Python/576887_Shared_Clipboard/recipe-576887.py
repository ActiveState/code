#!/usr/bin/python2.5
# -*- coding: utf-8 -*-
""" A shared clipboard using a network accessible file. Inspired by [1] but
supports Linux, unicode, and interrupting (if paused virtual machine).

[1]:http://www.devx.com/opensource/Article/37233/1954
"""

import codecs
import os
try: # use killable process because xsel/xclip sometimes stalls
    from killableprocess import Popen # http://svn.smedbergs.us/python-processes/trunk/
except ImportError:
    from subprocess import Popen
from subprocess import PIPE

import signal
import sys
import time

#### Clipboard files and functions per system ####
# Mac stuff removed since I can't test, see [1] above.

if sys.platform == 'win32':
    clipboard_fn = r'w:\apps\clipboard\clipboard.txt'
    log_fn = r'w:\apps\clipboard\log_clipboard.txt'
    import win32clipboard

    def openClipboard():
        win32clipboard.OpenClipboard()
    def closeClipboard():
        try:
            win32clipboard.CloseClipboard()
        except Exception, e:
            print e
            pass
    def getClipboardData():
        from win32clipboard import CF_UNICODETEXT
        if win32clipboard.IsClipboardFormatAvailable(CF_UNICODETEXT):
            return win32clipboard.GetClipboardData().decode('cp1252')
        else:
            return None
    def setClipboardData(data): # “ Václav
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_UNICODETEXT,
            data)
            
elif sys.platform == 'linux2':
    clipboard_fn = r'/home/reagle/e/win/apps/clipboard/clipboard.txt'
    log_fn = r'/home/reagle/e/win/apps/clipboard/log_clipboard.txt'
    def openClipboard():
        pass
    def closeClipboard():
        pass
    def getClipboardData(): # xclip needs iso-8859-1 for ver < 0.11 #failed
        my_logger.debug('  %s: getClipboardData' % sys.platform)
        p = Popen(['/usr/bin/xsel', '-t', '200', '-o'], stdout=PIPE)
        p.wait(2)
        result = p.communicate()[0].decode('utf-8')
        my_logger.debug('  %s: gotClipboardData "%s"' % (sys.platform, result))
        return result
    def setClipboardData(data):
        my_logger.debug('  %s: setClipboardData data = "%s"' % (sys.platform, data))
        p = Popen(['/usr/bin/xsel', '-t', '200', '-i'], stdin=PIPE)
        result = p.communicate(input=data.encode('utf-8'))
        p.wait(2)
        my_logger.debug('  %s: setClipboardData done' % sys.platform)
        return result
else:
    print "Unknown system"
    sys.exit()


#### Logging ####
#import logging
#import logging.handlers
#my_logger = logging.getLogger('MyLogger')
#my_logger.setLevel(logging.DEBUG) # CRITICAL
#handler = logging.StreamHandler(sys.stderr)
##handler = logging.handlers.RotatingFileHandler(
            ##log_fn, maxBytes=2000, backupCount=0) # log_fn
#my_logger.addHandler(handler)

class Logger:
    def debug(self, msg):
        pass
        #now = time.localtime(time.time())
        #print time.strftime("%H%M%S", now) + msg.encode('utf-8')
my_logger = Logger()


#### File Object ####

class File:
    def __init__(self, clipboard_fn):
        self.prev_mtime = self.mtime = None
        self.clipboard_fn = clipboard_fn
    
    def hasUpdated(self):
        '''Checking file attribute lessens file blocking of read'''
        self.prev_mtime = self.mtime
        self.mtime = os.stat(self.clipboard_fn).st_mtime # last time clipboard_fn modified
        return self.mtime != self.prev_mtime

    def update(self):
        self.mtime = os.stat(self.clipboard_fn).st_mtime
        my_logger.debug('  %s: updated mtime "%s"' % (sys.platform, self.mtime))

    def write(self, data):
        my_logger.debug('  %s: opening clipboard_fn for write' % sys.platform)
        fd = codecs.open(self.clipboard_fn, 'w', 'utf-8')
        fd.write(data)
        fd.close()
        my_logger.debug('  %s: closed clipboard_fn for write' % sys.platform)
        my_logger.debug('  %s: wrote "%s"' % (sys.platform, data))

    def read(self):
        my_logger.debug('%s:  clipboard_fn updated, opening for read'  % sys.platform)
        fd = codecs.open(self.clipboard_fn, 'r', 'utf-8')
        data = fd.read()
        my_logger.debug("  %s: getting data = '%s'"  % (sys.platform, data))
        fd.close()
        my_logger.debug('  %s: closed clipboard_fn for read'  % sys.platform)
        return data

clipboard_file = File(clipboard_fn)


#### Poll clipboard loop #####

wait_no = 0

def monitorClipboard(clipboard_fn):
    prev_data = u''
    while (True):
        time.sleep(1)
        try:
            openClipboard()
        except:
            my_logger.debug('OpenClipboard() failed')
            continue
        
        try:
            data = getClipboardData()
            if data and data != prev_data:  # write to clipboard_fn
                my_logger.debug('\n\n%s:  update clipboard update: "%s" != "%s"'
                    % (sys.platform, data[0:10], prev_data[0:10]))
                clipboard_file.write(data)
                prev_data = data
                clipboard_file.update()
            else:   # local clipboard hasn't changed, did remote clipboard change?
                if clipboard_file.hasUpdated():
                    data = clipboard_file.read()
                    if data != prev_data: 
                        setClipboardData(data)
                        prev_data = data
            sys.stdout.flush()
        except Exception, e:
            my_logger.debug(str(e))
            time.sleep(5)   # for network upon resume: wait 5 seconds, 3 times
            wait_no += 1
            if wait_no == 3:
                sys.exit()
        else:
            wait_no = 0     # if suceeded, reset wait
        closeClipboard()

def main():
    monitorClipboard(clipboard_fn)

if __name__=='__main__':
    main()
