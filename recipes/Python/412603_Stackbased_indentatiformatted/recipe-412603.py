import logging, inspect
class IndentFormatter(logging.Formatter):
    def __init__( self, fmt=None, datefmt=None ):
        logging.Formatter.__init__(self, fmt, datefmt)
        self.baseline = len(inspect.stack())
    def format( self, rec ):
        stack = inspect.stack()
        rec.indent = ' '*(len(stack)-self.baseline)
        rec.function = stack[8][3]
        out = logging.Formatter.format(self, rec)
        del rec.indent; del rec.function
        return out

# USAGE:
formatter = IndentFormatter("[%(levelname)s]%(indent)s%(function)s:%(message)s")

logger = logging.getLogger('logger')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

TRON = logging.DEBUG + 1
logging.addLevelName(TRON, "TRON")
logger.setLevel(TRON)

logger.log(TRON, 'I am a logger')

def f3():
    logger.log(TRON, 'I am f3')
def f2():
    logger.log(TRON, 'I am f2')
    f3()
def f1():
    logger.log(TRON, 'I am f1')
    f2()
def go():
  logger.log(TRON, 'I am go.')
  f1()
  f2()
  f3()
f1()
go()
