# To run this code, create a python file, say config.py, with a sample parameter 
# called sample_param. 

import os
import sys

def main():

    if len(sys.argv) == 1:
        print "usage: %s config_file" % os.path.basename(sys.argv[0])
        sys.exit(2)

    config_file = os.path.basename(sys.argv[1])
    if config_file[-3:] == ".py":
        config_file = config_file[:-3]

    data_config = __import__(config_file, globals(), locals(), [])
    print data_config.sample_param

main()
