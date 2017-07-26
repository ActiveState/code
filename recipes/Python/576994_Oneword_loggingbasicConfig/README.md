## One-word logging.basicConfig wrapper

Originally published: 2010-01-06 06:53:29
Last updated: 2010-01-06 06:54:09
Author: Denis Barmenkov

Every Python logging manual have this code:\n\n    logging.basicConfig(level=logging.DEBUG, filename='debug.log',\n                        format='%(asctime)s %(levelname)s: %(message)s',\n                        datefmt='%Y-%m-%d %H:%M:%S')\n\nThis is a simple function which call it for you.\nAll you need is remember one function name; useful on little scripts.