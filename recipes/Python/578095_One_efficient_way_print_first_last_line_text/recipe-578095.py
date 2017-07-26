import os
import sys

def print_first_last_line(inputfile) :
    filesize = os.path.getsize(inputfile)
    blocksize = 1024
    dat_file = open(inputfile, 'rb')
    headers = dat_file.readline().strip()
    if filesize > blocksize :
        maxseekpoint = (filesize // blocksize)
        dat_file.seek(maxseekpoint*blocksize)
    elif filesize :
        maxseekpoint = blocksize % filesize
        dat_file.seek(maxseekpoint)    
    lines =  dat_file.readlines()    
    if lines :
        last_line = lines[-1].strip()
    print "first line : ", headers
    print "last line : ", last_line

if __name__ == "__main__" :
    if len(sys.argv) >= 2:
        print_first_last_line(sys.argv[1])
    else:
        sys.exit("Usage %s filename" % sys.argv[0])
