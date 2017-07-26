## One-word logging.basicConfig wrapper  
Originally published: 2010-01-06 06:53:29  
Last updated: 2010-01-06 06:54:09  
Author: Denis Barmenkov  
  
Every Python logging manual have this code:

    logging.basicConfig(level=logging.DEBUG, filename='debug.log',
                        format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

This is a simple function which call it for you.
All you need is remember one function name; useful on little scripts.