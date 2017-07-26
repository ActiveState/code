import logging
import sys
import inspect

def log_assert(bool_, message="", logger=None, logger_name="", verbose=False):
    """Use this as a replacement for assert if you want the failing of the
    assert statement to be logged."""
    if logger is None:
        logger = logging.getLogger(logger_name)
    try:
        assert bool_, message
    except AssertionError:
        # construct an exception message from the code of the calling frame
        last_stackframe = inspect.stack()[-2]
        source_file, line_no, func = last_stackframe[1:4]
        source = "Traceback (most recent call last):\n" + \
            '  File "%s", line %s, in %s\n    ' % (source_file, line_no, func)
        if verbose:
            # include more lines than that where the statement was made
            source_code = open(source_file).readlines()
            source += "".join(source_code[line_no - 3:line_no + 1])
        else:
            source += last_stackframe[-2][0].strip()
        logger.debug("%s\n%s" % (message, source))
        raise AssertionError("%s\n%s" % (message, source))

def mr_barnard():
    this = "an argument"
    log_assert(this is not "an argument", 
               "Yes it is. - No it isn't. It's just contradiction.",
               verbose=True) 

if __name__ == "__main__":
    logging.basicConfig(filename="argument_clinic", level=logging.DEBUG)
    
    try:
        mr_barnard()  # room 12
    finally:
        print "What a stupid concept."
