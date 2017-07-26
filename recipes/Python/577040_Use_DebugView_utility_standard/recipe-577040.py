# DbgViewHandler for Python's standard logging module
# For information on DebugView see http://technet.microsoft.com/en-us/sysinternals/bb896647.aspx

import logging
from win32api import OutputDebugString

class DbgViewHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)
        
    def emit(self, record):
        OutputDebugString(self.format(record))

        
if __name__ == '__main__':     
    
    # example
    log = logging.getLogger()
    log.addHandler(DbgViewHandler())
    log.warn('test a warning message')   
