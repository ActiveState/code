#!/usr/bin/env python

import os
import sys
from logging import Logger
import daemon

class FileLikeLogger:
    "wraps a logging.Logger into a file like object"

    def __init__(self, logger):
        self.logger = logger

    def write(self, str):
        str = str.rstrip() #get rid of all tailing newlines and white space
        if str: #don't log emtpy lines
            for line in str.split('\n'):
                self.logger.critical(line) #critical to log at any logLevel

    def flush(self):
        for handler in self.logger.handlers:
            handler.flush()

    def close(self):
        for handler in self.logger.handlers:
            handler.close()

def openFilesFromLoggers(loggers):
    "returns the open files used by file-based handlers of the specified loggers"
    openFiles = []
    for logger in loggers:
        for handler in logger.handlers:
            if hasattr(handler, 'stream') and \
               hasattr(handler.stream, 'fileno'):
                openFiles.append(handler.stream)
    return openFiles
      
class LoggingDaemonContext(daemon.DaemonContext):

    def _addLoggerFiles(self):
        "adds all files related to loggers_preserve to files_preserve"
        for logger in [self.stdout_logger, self.stderr_logger]:
            if logger:
                self.loggers_preserve.append(logger)
        loggerFiles = openFilesFromLoggers(self.loggers_preserve)
        self.files_preserve.extend(loggerFiles)

    def __init__(
        self,
        chroot_directory=None,
        working_directory='/',
        umask=0,
        uid=None,
        gid=None,
        prevent_core=True,
        detach_process=None,
        files_preserve=[],   # changed default
        loggers_preserve=[], # new
        pidfile=None,
        stdout_logger = None,  # new
        stderr_logger = None,  # new
        #stdin,   omitted!
        #stdout,  omitted!
        #sterr,   omitted!
        signal_map=None,
        ):

        self.stdout_logger = stdout_logger
        self.stderr_logger = stderr_logger
        self.loggers_preserve = loggers_preserve

        devnull_in = open(os.devnull, 'r+')
        devnull_out = open(os.devnull, 'w+')
        files_preserve.extend([devnull_in, devnull_out])

        daemon.DaemonContext.__init__(self,
            chroot_directory = chroot_directory,
            working_directory = working_directory,
            umask = umask,
            uid = uid,
            gid = gid,
            prevent_core = prevent_core,
            detach_process = detach_process,
            files_preserve = files_preserve, 
            pidfile = pidfile,
            stdin = devnull_in,
            stdout = devnull_out,
            stderr = devnull_out,
            signal_map = signal_map) 

    def open(self): 
        self._addLoggerFiles() 
        daemon.DaemonContext.open(self)
        if self.stdout_logger:
            fileLikeObj = FileLikeLogger(self.stdout_logger)
            sys.stdout = fileLikeObj
        if self.stderr_logger:
            fileLikeObj = FileLikeLogger(self.stderr_logger)
            sys.stderr = fileLikeObj


#---------------------------------------------------------------
if __name__ == '__main__':

    # since this test uses chroot, it should be called as superuser (sudo..)

    import logging
    import logging.handlers
    import random
    import time
    import urllib2

    #-- setting up a rotating file logger -------
    def getRotFileLogger(name, filePath, logLevel=logging.DEBUG, format=None):
        format = format or '%(message)s'
        my_logger = logging.getLogger(name)
        my_logger.setLevel(logLevel)
        handler = logging.handlers.RotatingFileHandler(
                      filePath, maxBytes=2000, backupCount=2)
        formatter = logging.Formatter(format)
        handler.setFormatter(formatter)
        my_logger.addHandler(handler)
        return my_logger

    #-- some utilities ---
    def rmTestFiles(*fList):
        for f in fList:
            rmTestFile(f)

    def rmTestFile(fileName):
        if os.path.isfile(fileName):
            os.remove(fileName)

    def rmTestDir(dirName):
        if os.path.isdir(dirName):
            os.rmdir(dirName)

    #-- clean up the test directory and file structure ----
    rmTestFile('jail/beacon.txt')
    rmTestFile('jail/jailTestFile.txt')
    rmTestDir('jail')
    rmTestFiles('test.log', 'stdout.log', 'stderr.log', 'test.file')
    os.mkdir(os.path.join(os.getcwd(), 'jail'))
    open('jail/beacon.txt', 'w').write('I should be found')

    #-- set up loggers and files for the daemon
    testLogger = getRotFileLogger('test', 'test.log')
    stdoutLogger = getRotFileLogger('stdout', 'stdout.log')
    stderrLogger = getRotFileLogger('stderr', 'stderr.log')
    testFile = open('test.file', 'w')

    #-- test that all work before opening the DaemonContext
    testLogger.info('testLogger: before opening context')
    stdoutLogger.info('stdoutLogger: before opening context')
    stderrLogger.info('stderrLogger: before opening context')
    testFile.write('testFile: hello to a file before context\n')

    #-- get and configure the DaemonContext
    context = LoggingDaemonContext()
    context.files_preserve=[testFile]
    context.loggers_preserve=[testLogger]
    context.stdout_logger = stdoutLogger
    context.stderr_logger = stderrLogger
    context.chroot_directory = os.path.join(os.getcwd(), 'jail')

    #-- test whether it all works
    with context:
        # should appear in stdout.log
        print "stdout: hello!"
        # should appear in test.log
        testLogger.info('testLogger: hello, just testing')
        # should appear in test.file
        testFile.write('testFile: hello to a file\n')

        #testing chroot
        print "If chroot works, I should see beacon.txt: %s" % os.listdir('.')
        open('jailTestFile.txt', 'w').write('this was written in the jail\n')
        # do these things need access to devices???:
        print "time is: %s" % time.time() 
        print "this is a random number: %s" % random.randint(1, 100)
        # the above seems to work without errors
        # but the following needs access to devices that are not available in the jail
        print urllib2.urlopen('http://www.python.org/').read(20)

        # should appear in stderr.file
        raise (Exception("stderrLogger: bummer!"))
