import socket; socket.setdefaulttimeout(60)
import Queue # 2.5 module required
import random, time, sys, threading, posixpath, traceback, os
import ftplib

DEFNUMWORKERS = 20          # max active connections
DEFMAXSIZE = 32*1024*1024   # for splitting file
DEFBLOCKSIZE = 32*1024      # for downloading

class JobQueue(Queue.Queue):
    def get(self, block=True, timeout=None):
        item = Queue.Queue.get(self, block, timeout)
        print_('got: %r\n' % (item,))
        return item
    
    def put(self, item, block=True, timeout=None):
        Queue.Queue.put(self, item, block, timeout)
        print_('new (of %s jobs): %r\n' % (self.unfinished_tasks, item))

    def task_done(self):
        Queue.Queue.task_done(self)
        print_('job count: %s\n' % self.unfinished_tasks)

def main(host, user, passwd, src,
         numworkers=DEFNUMWORKERS,
         maxsize=DEFMAXSIZE,
         blocksize=DEFBLOCKSIZE):

    map(assert_positive_int, (numworkers, maxsize, blocksize))
    
    getconn = lambda: ftplib.FTP(host, user, passwd)
    
    srcdir, srcfile = posixpath.split(src)
    dst = os.path.join(os.curdir, srcfile)
    totalsize = get_source_size(getconn, srcdir, srcfile)
    allocate_diskspace(dst, totalsize)    
    jobs = split_job(totalsize, maxsize)
    
    bc = ByteCounter(totalsize)
    open_ = lambda: WrappedWrite(open(dst, 'rb+'), bc)
    
    jobqueue = JobQueue()
    for offset, size in jobs: jobqueue.put((offset, size))

    for _ in range(numworkers):
        t = threading.Thread(
            target=downloader,
            args=(jobqueue, getconn, src, open_, blocksize)
            )
        t.setDaemon(True)
        t.start()

    jobqueue.join()

def downloader(jobqueue, connect, src, open_, blocksize):
    while True:
        job = jobqueue.get()
        try:
            srcdir, srcfile = posixpath.split(src)
            (offset, size) = job
            try:
                fp = open_()
                try:
                    fp.seek(offset)
                    ftp = connect()
                    try:
                        ftp.cwd(srcdir)
                        ftp.voidcmd('TYPE I')
                        sock, _ = ftp.ntransfercmd('RETR %s' % srcfile, offset)
                        try: receive(sock, fp.write, size, blocksize)
                        finally: sock.close()
                        
                        try: # ignore errors here as we already received bytes
                            print_('%s\n' % ftp.getmultiline())
                            ftp.putcmd('ABOR')
                            print_('%s\n' % ftp.getmultiline())
                        except: pass
                        
                    finally: ftp.close()
                finally:
                    diff = get_size_diff(fp, offset)
                    newoffset, newsize = offset+diff, size-diff
                    fp.close()

            except:
                if newsize>0: jobqueue.put((newoffset, newsize))
                error_callback()

            else: print_('%r OK\n' % ((offset, size),))

        finally: jobqueue.task_done()

def receive(sock, callback, size, blocksize):
    length = 0
    remaining = size
    
    while True:
        buffsize = min((blocksize, remaining))
        if buffsize<=0: break # if remaining<=0: break
        data = sock.recv(buffsize)
        if not data: break
        callback(data)
        received = len(data)
        length += received
        remaining -= received
        assert (size-length)==remaining, (size, length, remaining)
        if length>=size: break

    sock.shutdown(socket.SHUT_RDWR) # needed? or perhaps socket.SHUT_RD?
    if size!=length: raise UnexpectedDataLength(size, length)

def calc_count(totalsize, maxsize=DEFMAXSIZE):
    q, r = divmod(totalsize, maxsize)
    count = q+bool(r)
    return count

def calc_sizes(totalsize, count):
    q, r = divmod(totalsize, count)
    sizes = [q]*count
    sizes[0] += r
    return sizes

def calc_offsets(sizes):
    offsets = []
    pos = 0
    for s in sizes:
        offsets.append(pos)
        pos += s

    return offsets

def split_job(totalsize, maxsize=DEFMAXSIZE):
    count = calc_count(totalsize, maxsize)
    sizes = calc_sizes(totalsize, count)
    offsets = calc_offsets(sizes)
    return zip(offsets, sizes)

class ByteCounter(object):
    def __init__(self, size):
        self.size = size
        self.lock = threading.Lock()
        self.count = 0

    def inc(self, length):
        self.lock.acquire()
        try: self.count += length
        finally: self.lock.release()
        
class WrappedWrite(object):
    def __init__(self, fp, counter):
        self._fp, self._counter = fp, counter

    def write(self, string):
        self._counter.inc(len(string))
        return self._fp.write(string)

    def close(self):
        print_('%.2f%%\n' % (100.0*self._counter.count/self._counter.size))
        return self._fp.close()

    def __getattr__(self, name):
        return getattr(self._fp, name)

def get_size_diff(fp, offset):
    try: return max((0, fp.tell()-offset))
    except: return 0

def allocate_diskspace(path, size):
    assert_positive_int(size)
    f = open(path, 'wb')
    try: f.truncate(size) # need to check if this works on Linux et al
    finally: f.close()
    rsize = os.path.getsize(path)
    assert rsize==size, (rsize, size)

def get_source_size(connect, srcdir, srcfile):
    ftp = connect()
    try:
        ftp.cwd(srcdir)
        ftp.voidcmd('TYPE I')
        size = ftp.size(srcfile)
    finally: ftp.close()
    assert_positive_int(size)
    return size
    
def assert_positive_int(v):
    assert ((v>0) and (int(v)==v)), v

def get_threadname():
    try: return threading.currentThread().getName()
    except: return 'n.a.'

def get_error_traceback():
    errtype, errinst, tb = sys.exc_info()
    try:
        error = ''.join(traceback.format_exception_only(errtype, errinst))
        trace = ''.join(traceback.format_exception(errtype, errinst, tb))
        return error, trace
    finally: del tb

def TEP(func):
    def tep(*args, **kwargs):
        try: return func(*args, **kwargs)
        except: pass

    return tep        

@TEP
def error_callback():
    e, t = get_error_traceback()
    print_('%s\n' % (e.strip(),))
    print_(t, sys.stderr)

@TEP
def print_(s, stream=sys.stdout):
    stream.write(s)
    stream.flush()

class UnexpectedDataLength(ValueError):
    pass

def _test1():
    totalsize = 364388352
    maxsize = DEFMAXSIZE
    count = calc_count(totalsize, maxsize)
    assert (1.0*totalsize/count)<=maxsize
    sizes = calc_sizes(totalsize, count)
    assert sum(sizes)==totalsize
    offsets = calc_offsets(sizes)
    assert len(sizes)==len(offsets)
    assert offsets[-1]+sizes[-1]==totalsize

    from pprint import pprint
    pprint(zip(offsets, sizes))
    
def _test2():
    jobs = split_job(364388352)
    jobqueue = Queue.Queue()
    numworkers = 8
    
    for _ in range(numworkers):
        t = threading.Thread(target=_worker, args=(jobqueue,))
        t.setDaemon(True)
        t.start()

    for (offset, size) in jobs:
        jobqueue.put((offset, size))

    jobqueue.join()

    print_('all done.\n')

def _worker(jobqueue):
    while True:
        job = jobqueue.get()
        try:
            (offset, size) = job
            try:
                print_('%d\t%d\n' % (offset, size))
                time.sleep(random.randint(1, 3))
                if not random.choice([0, 1, 1]):
                    raise RuntimeError(offset, size)
                
            except:
                jobqueue.put((offset, size))
                print_('%r failed\n' % (job,))

            else:
                print_('%r OK\n' % (job,))

        finally: jobqueue.task_done()

if __name__ == '__main__':

    host = 'localhost'
    user = 'Justin Ezequiel'
    passwd = '******'
    src = '/cnet/VM-4-00-DEV/Windows 2000 Professional-000001-cl3.vmdk'

    workers, maxsize, blocksize = 20, 32*1024*1024, 32*1024

    s = time.time()
    main(host, user, passwd, src, workers, maxsize, blocksize)
    print 'Done in %.2f seconds' % (time.time()-s,)
