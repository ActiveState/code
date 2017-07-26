#! /usr/bin/env python3

"""
selflogger.py

Written by Geremy Condra

Licensed under GPLv3

Released 27 May 2009

This module contains a simple exception
designed to self-log.
"""

import logging
import traceback

class LoggingError(Exception):
        """Basic logging error"""
        
        # set the logging options
        filename = 'log'
        datefmt = '%a, %d %b %Y %H:%M:%S'
        format = '%(asctime)s %(levelname)-8s %(message)s'
        
        # build the logger
        logging.basicConfig(level=logging.DEBUG,
                            filename=filename,
                            datefmt=datefmt,
                            format=format)

        # and get a local variable for it
        log = logging.getLogger('')
                
        def __init__(self, *args):
                # build the message from the user
                user_msg = args[0] if args else "An error has occurred"
                # get the traceback from the last error if it exists
                try: tb = traceback.format_exc()
                # otherwise, get the tb prior to this frame and pretend its us
                except: 
                        tb = "Traceback (most recent call last):\n"
                        tb += ''.join(traceback.format_stack()[:-1])
                        tb += self.__class__.__name__ + ": " + user_msg
                        tb += '\n'
                # build the complete log message
                log_msg = user_msg + "\n" + tb
                # and log it
                self.log.error(log_msg)
                # store the args
                self.args = args


if __name__ == "__main__":

        # example 1: raise it all by itself
        raise LoggingError("AIEEE!")

        # example 2: using it to log a re-raise
        try: dict()[5]
        except: raise LoggingError
