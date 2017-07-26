import logging
import logging.handlers

    
def enable_logger_print():
    def _logger_str(self):
        s = ''
        if self.parent != None:
            s =  _logger_str(self.parent)
        s += """\n%s\n""" % (self.name)
        for name,value in self.__dict__.items():
            if name == 'parent': value = value and value.name or 'None'
            if name == 'level': value = '%s (%s)' %(value,logging.getLevelName(value))
            s += '    %s = %s\n' % (name,value)
        return s

    def _handler_repr(handlername):
        def __repr__(self):
            s = '\n\t%s\n' % (handlername)
            for name,value in self.__dict__.items():
                if name == 'level': value = '%s (%s)' %(value,logging.getLevelName(value))
                s += '\t    %s = %s\n' % (name,value)
            s += '\t'
            return s
        return __repr__

    def _formatter_repr(self):
        s = ""
        for name,value in self.__dict__.items():
            s += '\n\t\t%s = %s' % (name,value)
        return s

    def _manager_repr(self):
        s = ""
        for name,value in self.__dict__.items():
            if name == 'root': value = value.name
            if name == 'loggerDict': value = _logger_list(); name='loggerDict keys'
            s += '\n        %s = %s' % (name,value)
        return s

    def _filter_repr(self):
        return self.name

    def _logger_list():
        return sorted([name for name in logging.Logger.manager.loggerDict])

    for name in dir():
        if name.endswith('Handler'):
            logging.__dict__[name].__repr__ = _handler_repr(name)

    for name in dir(logging):
        if name.endswith('Handler'):
            logging.__dict__[name].__repr__ = _handler_repr(name)

    for name in dir(logging.handlers):
        if name.endswith('Handler'):
            logging.handlers.__dict__[name].__repr__ = _handler_repr(name)

    logging.Logger.__str__ = _logger_str
    logging.Formatter.__repr__ = _formatter_repr
    logging.Filter.__repr__ = _filter_repr
    logging.Manager.__repr__ = _manager_repr
        

if __name__ == '__main__':
    logging.basicConfig( level=logging.INFO)

    logger = logging.getLogger('')
    logger1 = logging.getLogger('a.b.c')
    logger2 = logging.getLogger('x.a')

    rootLogger = logging.getLogger()
    rootLogger.setLevel(logging.DEBUG)

    streamHandler = logging.StreamHandler()
    streamHandler.name = 'Stream Server'
    frmt = logging.Formatter("%(filename)s - %(name)s - %(levelname)s - %(message)s")
    streamHandler.setFormatter(frmt)
    fltr = logging.Filter('x')
    streamHandler.addFilter(fltr)
    logger.addHandler(streamHandler)

    print '='*80
    print '\n*** print logger2 BEFORE enable_logger_print() ***\n'
    print logger2
    print '='*80

    enable_logger_print() # allows printing logger internals

    print '\n*** print logger2 AFTER enable_logger_print() ***\n'
    print logger2
    print '='*80

    logger.info('Help Me (root)')
    logger1.info('Help Me (a.b.c)')
    logger2.info('Help Me (x)')
