import time, os, select, signal

class subProcess:
    """Class representing a child process. It's like popen2.Popen3
       but there are three main differences.
       1. This makes the new child process group leader (using setpgrp())
          so that all children can be killed.
       2. The output function (read) is optionally non blocking returning in
          specified timeout if nothing is read, or as close to specified
          timeout as possible if data is read.
       3. The output from both stdout & stderr is read (into outdata and
          errdata). Reading from multiple outputs while not deadlocking
          is not trivial and is often done in a non robust manner."""

    def __init__(self, cmd, bufsize=8192):
        """The parameter 'cmd' is the shell command to execute in a
        sub-process. If the 'bufsize' parameter is specified, it
        specifies the size of the I/O buffers from the child process."""
        self.cleaned=False
        self.BUFSIZ=bufsize
        self.outr, self.outw = os.pipe()
        self.errr, self.errw = os.pipe()
        self.pid = os.fork()
        if self.pid == 0:
            self._child(cmd)
        os.close(self.outw) #parent doesn't write so close
        os.close(self.errw)
        # Note we could use self.stdout=fdopen(self.outr) here
        # to get a higher level file object like popen2.Popen3 uses.
        # This would have the advantages of auto handling the BUFSIZ
        # and closing the files when deleted. However it would mean
        # that it would block waiting for a full BUFSIZ unless we explicitly
        # set the files non blocking, and there would be extra uneeded
        # overhead like EOL conversion. So I think it's handier to use os.read()
        self.outdata = self.errdata = ''
        self._outeof = self._erreof = 0

    def _child(self, cmd):
        # Note sh below doesn't setup a seperate group (job control)
        # for non interactive shells (hmm maybe -m option does?)
        os.setpgrp() #seperate group so we can kill it
        os.dup2(self.outw,1) #stdout to write side of pipe
        os.dup2(self.errw,2) #stderr to write side of pipe
        #stdout & stderr connected to pipe, so close all other files
        map(os.close,[self.outr,self.outw,self.errr,self.errw])
        try:
            cmd = ['/bin/sh', '-c', cmd]
            os.execvp(cmd[0], cmd)
        finally: #exit child on error
            os._exit(1)

    def read(self, timeout=None):
        """return 0 when finished
           else return 1 every timeout seconds
           data will be in outdata and errdata"""
        currtime=time.time()
        while 1:
            tocheck=[]
            if not self._outeof:
                tocheck.append(self.outr)
            if not self._erreof:
                tocheck.append(self.errr)
            ready = select.select(tocheck,[],[],timeout)
            if len(ready[0]) == 0: #no data timeout
                return 1
            else:
                if self.outr in ready[0]:
                    outchunk = os.read(self.outr,self.BUFSIZ)
                    if outchunk == '':
                        self._outeof = 1
                    self.outdata += outchunk
                if self.errr in ready[0]:
                    errchunk = os.read(self.errr,self.BUFSIZ)
                    if errchunk == '':
                        self._erreof = 1
                    self.errdata += errchunk
                if self._outeof and self._erreof:
                    return 0
                elif timeout:
                    if (time.time()-currtime) > timeout:
                        return 1 #may be more data but time to go

    def kill(self):
        os.kill(-self.pid, signal.SIGTERM) #kill whole group

    def cleanup(self):
        """Wait for and return the exit status of the child process."""
        self.cleaned=True
        os.close(self.outr)
        os.close(self.errr)
        pid, sts = os.waitpid(self.pid, 0)
        if pid == self.pid:
            self.sts = sts
        return self.sts

    def __del__(self):
        if not self.cleaned:
            self.cleanup()
