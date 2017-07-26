import logging

# adjust config to your own preferences
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename='myapp.log',
                    filemode='w')

class LoggingException(Exception):
    logger = logging.getLogger()
    logLevel = logging.ERROR

    def __init__(self):
        self.logger.log(self.logLevel, self.logMessage())

    def logMessage(self):
        return 'Exception occured'


if __name__ == '__main__':
    class BlewIt(LoggingException):
        logLevel = logging.WARNING
        def logMessage(self):
            return 'you blew it'
    try:
        raise BlewIt
    except:
        pass
