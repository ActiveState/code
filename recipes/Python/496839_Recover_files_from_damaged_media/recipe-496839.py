#!/usr/local/bin/python -O
# read faulty
# for each of its arguments, it tries to copy the faulty file to the cwd

import sys, os, errno
import collections
import cPickle as Pickle
import gzip

# use the correct errno reported per platform
if sys.platform == 'win32':
    read_failed= lambda exc: exc.errno == errno.EACCES
else:
    read_failed= lambda exc: exc.errno == errno.EIO

class Chunk(object):
    "A description of a data chunk to be read"
    UNIT= 2048
    BIG_UNIT= 32*UNIT

    def __init__(self, offset, size):
        self.offset= offset
        self.size= size

    def next_attempt(self):
        "Return sequence of chunks to retry"
        if self.size == self.UNIT: # a single sector failed
             yield self # try again in the next phase
        else:
            for ix in xrange(self.offset, self.offset+self.size, self.UNIT):
                yield self.__class__(ix, self.UNIT)

    def __getstate__(self):
        return self.offset, self.size
    def __setstate__(self, tpl):
        self.offset, self.size= tpl

    def description(self):
        "Return textual description of chunk"
        unit1= self.offset / self.UNIT
        unit2= (self.offset+self.size) / self.UNIT - 1
        if unit1 == unit2:
            return "%dMiB:%d" % (self.offset//1048576, unit1)
        else:
            return "%dMiB:%d-%d" % (self.offset//1048576, unit1, unit2)

class SuspectFile(object):
    "A file to be copied"
    destination= "."

    def __init__(self, filename, destination=None):
        # phase 1 contains big chunks to be read
        # phase 2 contains sectors to re-read
        # phase 3 contains chunks to store as completely failed
        self.filename= filename
        if destination is not None:
            self.destination= destination
        self.state_filename= os.path.basename(filename) + ".state"
        self.phase3= collections.deque()
        try:
            self.read_last_attempt_state()
        except IOError: # state file does not exist
            self.phase1= self.chunks_to_read()
            self.phase2= collections.deque()

    def chunks_to_read(self):
        result= collections.deque()
        filesize= os.path.getsize(self.filename)
        for offset in xrange(0, filesize, Chunk.BIG_UNIT):
            result.append(Chunk(
                offset,
                filesize-offset>Chunk.BIG_UNIT
                and Chunk.BIG_UNIT
                or filesize-offset))
        return result

    def record_state(self):
        if self.phase1 or self.phase2 or self.phase3:
            fpr= gzip.open(self.state_filename, "wb")
            Pickle.dump(self.phase1, fpr, -1)
            dummy_deque= collections.deque()
            dummy_deque.extend(self.phase2)
            dummy_deque.extend(self.phase3)
            Pickle.dump(dummy_deque, fpr, -1)
            fpr.close()
        else:
            try: os.remove(self.state_filename)
            except OSError: pass # ignore non-existant filename

    @staticmethod
    def copy_chunk(fpi, fpo, chunk):
        fpi.seek(chunk.offset)
        data= fpi.read(chunk.size)
        if data:
            fpo.seek(chunk.offset)
            fpo.write(data)
        return data

    def read_last_attempt_state(self):
        fpr= gzip.open(self.state_filename, "rb")
        self.phase1= Pickle.load(fpr)
        self.phase2= Pickle.load(fpr)

    # the report_* methods are to be overloaded
    def report_attempt(self, chunk):
        "This is to be overloaded with a way to report progress"
        pass

    def report_success(self, chunk):
        pass

    def report_failure(self, chunk):
        pass

    def phase_copy(self, fpi, fpo, phase_in, phase_out):
        "Copy chunks from fpi to fpo storing failures in phase_out"
        while phase_in:
            chunk= phase_in.popleft()
            try: # to make sure this chunk is not skipped, eg by KeyboardInterrupt
                self.report_attempt(chunk)
                try:
                    self.copy_chunk(fpi, fpo, chunk)
                except IOError, exc:
                    if read_failed(exc): # the way windows reports failure
                            for new_chunk in chunk.next_attempt():
                                phase_out.append(new_chunk)
                            chunk= None
                            self.report_failure(chunk)
                    else:
                        raise
                else:
                    # report success, but first make sure chunk is None
                    _, chunk= chunk, None
                    self.report_success(_)
            finally:
                if chunk: phase_in.appendleft(chunk)
                
    def copy(self):
        "Copy the file to the local directory"
        fpi= open(self.filename, "rb")
        fpo_filename= os.path.join(
            self.destination, os.path.basename(self.filename))
        try:
            fpo= open(fpo_filename, "r+b")
        except IOError, exc:
            if exc.errno == errno.ENOENT:
                fpo= open(fpo_filename, "wb")
            else:
                raise
        try:
            self.phase_copy(fpi, fpo, self.phase1, self.phase2)
            self.phase_copy(fpi, fpo, self.phase2, self.phase3)
        finally:
            self.record_state()

if __name__=="__main__":
    class SuspectFileCmd(SuspectFile):
        def report_attempt(self, chunk):
            sys.stderr.write(chunk.description())
        def report_success(self, chunk):
            sys.stderr.write("\r")
        def report_failure(self, chunk):
            sys.stderr.write(" failed\n")
        def record_state(self):
            super(SuspectFileCmd, self).record_state()
            sys.stderr.write("** remaining %d bytes in fast reads\n" % sum(chunk.size for chunk in self.phase1))
            sys.stderr.write("and %d sectors in re-reads\n" % (len(self.phase2) + len(self.phase3)) )

    for filename in sys.argv[1:]:
        faulty_file= SuspectFileCmd(filename)
        sys.stderr.write("copying %s\n" % filename)
        faulty_file.copy()
        sys.stderr.write("\n")
