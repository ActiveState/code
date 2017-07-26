#!/usr/bin/env python
#
# Copyright (c) 2014, Mike 'Fuzzy' Partin <fuzzy@fu-manchu.org>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the copyright holder nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL COPYRIGHT HOLDER BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

###########
## Stdlib

import os
import sys
import time
import urllib2
import urlparse
from curses import wrapper

####################
## Utility classes

class HumanReadable:

    def __init__(self):
        print('HumanReadable')

    def size(self, bytes=0):
        kbyte = 1024
        mbyte = (kbyte**2)
        gbyte = (kbyte**3)
        tbyte = (kbyte**4)
        pbyte = (kbyte**5)
        ebyte = (kbyte**6)
        zbyte = (kbyte**7)

        if bytes < kbyte: 
            retv = '%dB' % int(bytes)
            return '%9s' % retv
        elif bytes >= kbyte and bytes < mbyte:
            retv = '%04.02fKB' % (float(bytes) / float(kbyte))
            return '%9s' % retv
        elif bytes >= mbyte and bytes < gbyte:
            retv = '%04.02fMB' % (float(bytes) / float(mbyte))
            return '%9s' % retv
        elif bytes >= gbyte and bytes < tbyte:
            retv = '%04.02fGB' % (float(bytes) / float(gbyte))
            return '%9s' % retv
        elif bytes >= tbyte and bytes < pbyte:
            retv = '%04.02fTB' % (float(bytes) / float(tbyte))
            return '%9s' % retv
        elif bytes >= pbyte and bytes < ebyte:
            retv = '%04.02fPB' % (float(bytes) / float(pbyte))
            return '%9s' % retv
        elif bytes >= ebyte and bytes < zbyte:
            retv = '%04.02fEB' % (float(bytes) / float(ebyte))
            return '%9s' % retv
        else:
            retv = '%04.02fZB' % (float(bytes) / float(zbyte))
            return '%9s' % retv

    def time(self, seconds=0):
        # These are for convenience
        minute = 60
        hour   = (minute**2)
        day    = (hour*24)
        week   = (day*7)
        month  = (week*4)
        year   = (month*12)

        secs, mins, hrs, days, weeks, months, years = 0, 0, 0, 0, 0, 0, 0

        if seconds > year:
            years   = (seconds / year)
            tmp     = (seconds % year)
            seconds = tmp
        if seconds > month:
            months  = (seconds / month)
            tmp     = (seconds % month)
            seconds = tmp
        if seconds > week:
            weeks   = (seconds / week)
            tmp     = (seconds % week)
            seconds = tmp
        if seconds > day:
            days    = (seconds / day)
            tmp     = (seconds % day)
            seconds = tmp
        if seconds > hour:
            hrs     = (seconds / hour)
            tmp     = (seconds % hour)
            seconds = tmp
        if seconds > minute:
            mins    = (seconds / minute)
            secs    = (seconds % minute)
        if seconds < minute:
            secs   = seconds

        if years != 0:
            return '%4dy%2dm%1dw%1dd %02d:%02d:%02d' % (
                years, months, weeks, days, hrs, mins, secs
            )
        if months != 0:
            return '%2dm%1dw%1dd %02d:%02d:%02d' % (
                months, weeks, days, hrs, mins, secs
            )
        if weeks != 0:
            return '%1dw%1dd %02d:%02d:%02d' % (
                weeks, days, hrs, mins, secs
            )
        if days != 0:
            return '%1dd %02d:%02d:%02d' % (days, hrs, mins, secs)
        
        return '%02d:%02d:%02d' % (hrs, mins, secs)

class Output(HumanReadable):
    def __init__(self):
        self.display_flag  = True
        self.display_count = None

        # This is the most portable way (across POSIX systems) to get
        # our screen size that I can find, so, screw windows. Yeah.
        wrapper(self.__setmaxyx)

    def __setmaxyx(self, stdscr):
        (self.max_y, self.max_x) = stdscr.getmaxyx()


    def display(self, inTot=None, inSz=None, outSz=None, start_time=None):
        try:
            a = self.lastupdate
        except AttributeError:
            self.lastupdate = (time.time() - 5)
            
        if inTot:
            remain  = (inTot - outSz)
            percent = (float(outSz) / float(inTot))
            elapsed = (time.time() - start_time)
            speed   = (float(outSz) / float(elapsed))
            eta     = int(remain / speed)
                
            # now build out the majority of the display string
            linest  = '%s in %s @ %s/sec [' % (
                self.size(outSz),
                self.time(elapsed),
                self.size(speed)
            )
            lineend = '] %3d%% eta %s' % (
                int(percent * 100),
                self.time(eta)
            )
            
            # now figure out how many hashmarks we need
            curlen  = (len(linest)+len(lineend))
            hashlen = (self.max_x - curlen)
            hashes  = int(hashlen * percent)
            padding = (hashlen - hashes)
                
            # and put the line together
            line    = '%s%s%s%s' % (
                linest,
                '#'*hashes,
                ' '*padding,
                lineend
            )

        else:
            line = '%s in %s @ %s/sec' % (
                self.size(outSz),
                self.time(time.time() - start_time),
                self.size((outSz / (time.time() - start_time)))
            )

        if (time.time() - self.lastupdate) >= 1 and not self.quiet:
            sys.stderr.write('%s\r' % line)
            sys.stderr.flush()
            self.lastupdate = time.time()

################
## I/O classes

class Io:
    def _validateTarget(self, target=None):
        # First lets see if this is a legit path/file
        if os.path.exists(target):
            return True
        result = urlparse.urlparse(target)
        if result.scheme in ['http', 'https', 'ftp', 'ftps', 'scp', 'sftp', 'file']:
            return True
        return False

    def close(self):
        self.target.close()

    def read(self, bsize=40960):
        return self.target.read(bsize)

    def write(self, data):
        return self.target.write(data)

    def seek(self, pos=None):
        if pos:
            return self.target.seek(pos)                

class FileIo(Io):
    def __init__(self, target=None, mode=None):
        if not self._validateTarget(target):
            mode = 'w+'
        self.target = open(target, mode)
        if self.target.name != '/dev/stdout' and self.target.name != '/dev/stdin':
            self.size  = os.stat(self.target.name).st_size
            self.pipe  = False
        else:
            self.size  = None
            self.pipe  = True

class FifoIo(FileIo):
    pass

class HttpIo(Io):
    def __init__(self, target=None):
        self._validateTarget(target)
        self.target = urllib2.urlopen(target)

class FtpIo(HttpIo):
    pass

class ScpIo(Io):
    def __init__(self, bsize=10240, skip=0):
        pass

###################
## Transfer class

class Transfer(Output):
    def __init__(
            self,
            src=None,
            dst=None,
            tsize=None,
            bsize=40960,
            count=None,
            skip=None,
            quiet=False
    ):
        Output.__init__(self)
        self.src   = src
        self.dst   = dst
        self.bsize = bsize
        self.tsize = tsize
        self.count = count # TODO: Impliment
        self.skip  = skip  # TODO: Impliment
        self.quiet = quiet
        # Lets set our total size for display purposes
        if self.count:
            self.src.size = (self.bsize * self.count)
        # if we have set our total_size via an argument, lets go ahead, and set that
        try:
            if self.tsize:
                self.src.size = self.tsize
            elif not self.tsize and not os.path.isfile(self.src.target.name):
                self.src.size = -1
        except AttributeError:
            self.src.size = int(self.src.target.headers['content-length'])
        except:
            self.src.size = -1

    def start(self):
        blocks = 0
        totsze = 0

        try:
            st     = time.time()
            buff   = self.src.read(self.bsize)
            while buff:
                if totsze <= self.src.size or self.src.size == -1:
                    self.dst.write(buff)
                    blocks += 1
                    totsze += len(buff)
                    if self.src.size != -1:
                        self.display(self.src.size, totsze, totsze, st)
                    else:
                        self.display(None, totsze, totsze, st)
                    buff    = self.src.read(self.bsize)
                else:
                    buff    = None
            time.sleep(1)
            self.display(self.src.size, self.src.size, self.src.size, st)
            print
        except KeyboardInterrupt:
            print
            sys.exit(1)

#######################
## Main program entry

if __name__ == '__main__':
    # defaults
    iput  = FileIo('/dev/stdin', 'r')
    oput  = FileIo('/dev/stdout', 'a')
    ts    = None
    bs    = 40960 # 40KB
    count = None
    skip  = None
    quiet = False

    # help documentation
    usage = '''
Usage: %s <arg> <arg> ...

Arguments:

  if=<arg>      Set the input source
     /dev/stdin        # Default
     /path/to/file     # Set a path to a file or fifo
     (f|ht)tp(s)://uri # Use a remote location via http(s)/ftp(s)          (INPUT ONLY)
     scp://u@h:f       # Use SCP to get the file                           (TODO)

  of=<arg>      Set the output destination
     /dev/stdout       # Default
     /path/to/file     # Output to a file, device, fifo, socket file, etc.

  bs=<arg>      Specify the blocksize (in bytes only: Default 40960)
  ts=<arg>      Specify the total size in bytes (for use with pipes)
  count=<arg>   Specify how many blocks to transfer
  seek=<arg>    Seek <arg> number of blocks(bs) before reading data.
  quiet         Specify no progress output.
  help          Show this help screen.

''' % os.path.basename(sys.argv[0])

    # Parse out our arguments
    for arg in sys.argv:
        # Boolean args
        if arg == 'help':
            print(usage)
            sys.exit(0)
        if arg == 'quiet':
            quiet = True
        # Option args
        if arg.find('=') != -1:
            # this is a arg=opt style option, let's see which one.
            (key, val) = arg.split('=')
            if key == 'if': # input, see if it's a file
                if os.path.isfile(val):
                    iput = FileIo(val, 'r')
                else:
                    if val.find('http'):
                        iput = HttpIo(val)
                        oput = FileIo('./%s' % os.path.basename(val))
                    elif val.find('ftp'):
                        iput = FtpIo(val)
                        oput = FileIo('./%s' % os.path.basename(val))
                        
            if key == 'of': # output, see if it's a file
                oput = FileIo(val, 'w+')
            if key == 'bs':
                bs    = int(val)
            if key == 'ts':
                ts    = int(val)
            if key == 'count':
                count = int(val)
            if key == 'skip':
                skip  = int(val)
    
    obj = Transfer(iput, oput, ts, bs, count, skip, quiet)
    obj.start()
