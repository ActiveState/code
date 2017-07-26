#!/usr/bin/env python

# importLogsM.py - Matt Keranen 2011 (mksql@yahoo.com)

import os, getpass, logging, multiprocessing, sys, time, traceback
import logImport # The import script written to import a single file

# Add logging to current execution path, formatter set to match multiprocessing logger
logger = multiprocessing.log_to_stderr()
logger.setLevel(logging.INFO)

logf = os.path.join(sys.path[0], os.path.splitext(sys.argv[0])[0]+'.log')
filelog = logging.FileHandler(filename=logf)
filelog.setLevel(logging.INFO)
filelog.setFormatter(logging.Formatter('[%(levelname)s/%(module)s %(funcName)s] %(asctime)s | %(message)s'))
logger.addHandler(filelog)

def mapImport(infile, dstpath, server, engine, database, uid, pwd):
# Pass multiple args to import from mapped file list (Python 2.6)
    logImport.logger = logger 

    rc = logImport.importMP(infile, server, engine, database, uid, pwd)
    if rc > 0:
        try: os.rename(infile, os.path.join(dstpath, os.path.split(infile)[1]))
        except:
            logger.error("Error: %s" % traceback.format_exc(1))
            raise

    return rc

def mapArgs(args):
    return mapImport(*args)

if __name__ == '__main__':
    uid = 'import'
    pwd = getpass.getpass('Password for %s: ' % uid)

    src = 'F:\\import\\logs\\2011\\08'
    dst = 'F:\\import\\logs\\complete'

    jobs = []
    args = [dst, 'localhost', 's', 'testdb', uid, pwd]
    for root, dirs, files in os.walk(src):
        for name in files:
            jobs.append([os.path.join(root, name)] + args)

    if len(jobs) > 0:
        logger.info('Queueing %s files' % len(jobs))

        rc = []
        stime = time.time()
        pool = multiprocessing.Pool(4)
        try:
            rc = pool.map(mapArgs, jobs)
            pool.close()
            pool.join()
        except KeyboardInterrupt:  # http://jessenoller.com/2009/01/08/multiprocessingpool-and-keyboardinterrupt
            print('\nKeyboardInterrupt caught - terminating')
            pool.terminate()
            sys.exit()
        except:
            logger.error("Error: %s" % traceback.format_exc(1))
            pool.terminate()
            sys.exit()

        runtime = (time.time()-stime)+.001  # Avoid div/0

        logger.info('Complete: %d rows, %d sec (%d r/s)' % (sum(rc), runtime, sum(rc)/runtime))
