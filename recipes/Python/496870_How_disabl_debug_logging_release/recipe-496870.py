import logging

__orig_getLogger=None

def release_getLogger(name):
    '''
    passing original handler with debug() method replaced to empty function
    '''

    def dummy(*k, **kw):
        pass

    global __orig_getLogger
    log = __orig_getLogger(name)
    setattr(log, 'debug', dummy)
    return log

def install_release_loggers():
    '''
    save original handler, install newer
    '''
    global __orig_getLogger
    __orig_getLogger = logging.getLogger
    setattr(logging, 'getLogger', release_getLogger)

def restore_getLogger():
    '''
    restore original handler
    '''
    global __orig_getLogger
    if __orig_getLogger:
        setattr(logging, 'getLogger', __orig_getLogger)
        
# sample code
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(name)s %(levelname)s> %(message)s',
                    filename='./test.log',
                    filemode='w')

# start main program, install wrapper
install_release_loggers()

log = logging.getLogger('main')

log.info('=== start ===')
log.debug('hidden message ;)')
log.info('info')
log.error('mandatory error')

"""
Log will contain (without debug message):

main INFO> === start ===
main INFO> info
main ERROR> mandatory error
"""
