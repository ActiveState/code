#!/bin/env python
# coding:utf-8
# vim:ts=4:enc=utf-8

"""
Simple batch file processing module

Format of batch file:

    - A # is a comment delimiter, ignore everything on the line.
    - Anything else is command to run - no line continuations!
    
    You can basically just use a list of commands understood
    by the shell.

Example batch file:

    echo "Cmd 1" # this is a comment
    df -h
    # this is a comment too
    ls -lh

    echo "Cmd 4"

Simple, eh?

ver 1.1 - slight cleanup
ver 1.2 - remove interactive jobs (causing some bugs),
          rename variables to be more intuitive, add comments

If you really want to have interactive jobs, you could use
something like this bit of ugliness (but all on one line!):

    read -t 30 -p "Run command? [Y]"; if [ -z ${REPLY} ] || 
    [ ${REPLY} != "N" ]; then echo "I like cheese"; fi

ver 1.3 - minor cleanup
"""

import os
import sys

class SimpleBatchFile:
    """
    This is the main class
    
    Instantiate it then call run()
    """
    def _exec(self, command, jobnum, linenum, batchfile):
        """Execute a command in a subshell, die on errors"""
        print('     Starting job: %s\nExecuting command: %s\n' \
              % (jobnum, command))
        rv = os.system(command)
        if (rv):
            print('Problem running job...\n'
                  'File: %s\n'
                  ' Job: %d\n'
                  'Line: %d\n'
                  '...dieing!' % (batchfile, jobnum, linenum))
            sys.exit(rv)

    def __init__(self, batchfile):
        """Start the fun"""
        if not (os.path.isfile(batchfile)):
            print('Cannot find batch file: %s' % batchfile)
            sys.exit(1)
        self.file = batchfile
        fd        = open(batchfile, 'rb')
        data      = fd.readlines()
        fd.close()
        self.jobs = []
        for i in range(0, len(data)):
            item = data[i].strip()
            ## skip comments and empty lines
            if (item.startswith('#', 0, 1) or item == ''):
                continue
            ## format for jobs is (command, jobnum, linenum)
            self.jobs.append((item, len(self.jobs) + 1, i + 1))
        self.jobcount = len(self.jobs)

    def list(self):
        """List jobs and so forth"""
        for i in range(0, self.jobcount):
            if (i == 0):
                pad = ''
            else:
                pad = '========\n'
            print('%s    Job: %s\n   Line: %s\nCommand: %s' \
                    % (pad,
                       self.jobs[i][1],
                       self.jobs[i][2],
                       self.jobs[i][0]))

    def run(self, start=1, end=None):
        """
        to start from a given job use n, e.g., 3
        or to run a range of jobs use n:n, e.g., 3:5
        or for a single job only use n:n, e.g., 2:2
        no args means all jobs in batch are run
        """
        ## some bounds checking and logics
        if not (end):
            end = self.jobcount
        if (start < 1):
            start = 1
        if (start > self.jobcount):
            start = self.jobcount
        if (end > self.jobcount):
            end = self.jobcount
        if (end <= start):
            end = start
        for i in range(start - 1, end):
            self._exec(self.jobs[i][0],
                       self.jobs[i][1],
                       self.jobs[i][2],
                       self.file)

## end class SimpleBatchFile

if (__name__ == '__main__'):
    ## standalone script
    def get(lst, idx):
        """Return the value of lst[idx] or None"""
        if (len(lst) > idx):
            return lst[idx]
        else:
            return None
    ## get batch file name from argv
    bfnm = get(sys.argv, 1)
    ## no file given, print usage and exit
    if not (bfnm):
        me = os.path.basename(sys.argv[0])
        print('Usage: %s batch_file [start_job_number]' % me)
        sys.exit(1)
    ## instantiate class
    sbf  = SimpleBatchFile(bfnm)
    ## get range from argv
    scmd = get(sys.argv, 2)
    if not (scmd):
        ## run all jobs
        sbf.run()
    elif ('-l' in scmd):
        ## show job list
        sbf.list()
    elif (':' in scmd):
        ## run range of jobs
        scmd, ecmd = scmd.split(':')
        if not (ecmd):
            ecmd = 0
        sbf.run(int(scmd), int(ecmd))
    else:
        ## run all jobs including and after
        sbf.run(int(scmd))
