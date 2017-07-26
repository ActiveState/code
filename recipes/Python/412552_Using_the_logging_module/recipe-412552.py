import logging

class Opaque(logging.Filter):
    """A simple way to prevent any messages from getting through."""
    def __init__(self, name=None): pass
    def filter(self, rec): return False

class Unique(logging.Filter):
    """Messages are allowed through just once.
    The 'message' includes substitutions, but is not formatted by the 
    handler. If it were, then practically all messages would be unique!
    """
    def __init__(self, name=""):
        logging.Filter.__init__(self, name)
        self.reset()
    def reset(self):
        """Act as if nothing has happened."""
        self.__logged = {}
    def filter(self, rec):
        """logging.Filter.filter performs an extra filter on the name."""
        return logging.Filter.filter(self, rec) and self.__is_first_time(rec)
    def __is_first_time(self, rec):
        """Emit a message only once."""
        msg = rec.msg %(rec.args)
        if msg in self.__logged:
            self.__logged[msg] += 1
            return False
        else:
            self.__logged[msg] = 1
            return True

logging.warning("I am the root logger")
logging.getLogger().name = ""
logging.warning("I am the root logger")
logging.getLogger().name = "RootOfAllEvil" # You can use any name for the root.
logging.warning("I am the root logger")
logging.getLogger().name = "." # I like to use dot for the root
logging.warning("I am the root logger")
# Unfortunately, logging.getLogger() != logging.getLogger(".") # Bug?

logger = logging.getLogger(".child")
logger.warning("I am a child who repeats things.")
logger.warning("I am a child who repeats things.")

unique = Unique()
logger.addFilter(unique)
logger.warning("You only need to hear this once.")
logger.warning("You only need to hear this once.")

logger.warning("But this is worth repeating.")
unique.reset()
logger.warning("But this is worth repeating.")
logger.warning("But this is worth repeating.")

opaque = Opaque()
logger.addFilter(opaque)
logger.warning("You should never see this.")

logger.removeFilter(opaque)
logger.warning("You should see this just once.")
logger.warning("You should see this just once.")

sublogger = logging.getLogger(".child.grandchild")
sublogger.warning("This is not filtered by the parent logger.")
sublogger.warning("This is not filtered by the parent logger.")

handler = logging.StreamHandler()
formatter = logging.Formatter("EXTRA:%(name)s:'%(message)s'")
handler.setFormatter(formatter)
handler.addFilter(Unique()) #new instance of the Unique filter
logger.addHandler(handler)

sublogger.warning("But this *is* filtered by the parent's handlers.")
sublogger.warning("But this *is* filtered by the parent's handlers.")
