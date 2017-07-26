# -*- coding: Windows-1251 -*-
import datetime
import logging
import os
import sys

def quick_start_log(log_fn=None, mode=None, level=logging.DEBUG, \
                    format='%(asctime)s|%(name)s|%(levelname)s| %(message)s'):
    '''
    simplest basicConfig wrapper, open log file and return default log handler
    '''

    if log_fn is None:
        now = datetime.datetime.now()
        ts = now.strftime('%Y-%m-%d_%H%M%S')
        log_fn = '%s.%s.log' % (sys.argv[0], ts)

    if mode is None:
        mode = 'w'

    logging.basicConfig(level=level,
                        format=format,
                        filename=log_fn,
                        filemode=mode)

    logger = logging.getLogger('main')
    if mode.lower() == 'a':
        logger.info('---=== START ===---')

    return logger


if __name__ == '__main__':
    log = quick_start_log()
    log.info('message')
    log.fatal('exit')
