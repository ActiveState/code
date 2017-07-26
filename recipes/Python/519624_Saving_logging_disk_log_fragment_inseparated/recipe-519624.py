# -*- coding: Windows-1251 -*-
'''

'''
import logging
import os

log=logging.getLogger('LogExtractor')

BUF_SIZE=8*1024

class LogExtractor(object):
    '''
    Save current position of first disk file-based handler
    and save log fragment up to current position
    into separated file by request.

    Useful for splitting common program log for further reviewing
    by unprofessional personnel/client ;)
    '''

    def _find_file_handler(self, logger):
        # partially imported from Logger.callHandlers()
        c = logger
        filehandler=None
        while c:
            for hdlr in c.handlers:
                #log.info('Handler: %s' % type(hdlr))
                if isinstance(hdlr, logging.FileHandler):
                    filehandler=hdlr
                    break
            if filehandler:
                break

            if not c.propagate:
                c = None    #break out
            else:
                c = c.parent

        return filehandler

    def __init__(self, logger):
        '''
        search for first FileHandler and store it's current position 
        '''
        self.init_ok=0
        if not isinstance(logger, logging.Logger):
            log.error('__init__: <logger> must be instance of logging.Logger')
            return
        filehandler=self._find_file_handler(logger)
        if filehandler is None:
            log.error('__init__: no FileHandlers binded to <logger>')
            return
        self.stream=filehandler.stream
        self.basename=filehandler.baseFilename
        self.start_pos=self.stream.tell()
        self.init_ok=1

    def write_part(self, part_filename):
        '''
        put log file fragment from saved position to cyurrent state 
        into separate file
        '''
        if not self.init_ok:
            log.error('not properly initialized')
            return 0
        if self.stream.closed:
            if os.path.isfile(self.basename):
                part_size=os.path.getsize()
            else:
                log.error('log file (%s) not found on disk' % (self.basename))
                return 0
        else:
            part_size=self.stream.tell() - self.start_pos

        # put fragment
        f_log=open(self.basename, 'rb')
        f_part=open(part_filename, 'wb')
        try:
            f_log.seek(self.start_pos)
            left_size=part_size
            while left_size > 0:
                s=min(left_size, BUF_SIZE)
                buf=f_log.read(s)
                if len(buf) > 0:
                    f_part.write(buf)
                    left_size-=s
                else:
                    break
            return 1
        finally:
            f_part.close()
            f_log.close()

        return 0


if __name__ == '__main__':
    import sys

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s',
                        filename='%s.log' % sys.argv[0],
                        filemode='w')
    
    log=logging.getLogger('main')
    for i in range(1, 6):
        logextr=LogExtractor(log) # save current position

        for r in range(10):
            log.info('Pass %d: log message %d' % (i, r))

        rc=logextr.write_part('pass_%d.log' % i) # put fragment to file
        log.info('write_part result: %r' % rc)
