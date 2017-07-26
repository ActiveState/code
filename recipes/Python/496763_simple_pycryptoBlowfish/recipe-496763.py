#!/usr/bin/env python

import os, sys
from random import randrange
from Crypto.Cipher import Blowfish
from getpass import getpass
import getopt

class BFCipher:
    def __init__(self, pword):
        self.__cipher = Blowfish.new(pword)
    def encrypt(self, file_buffer):
        ciphertext = self.__cipher.encrypt(self.__pad_file(file_buffer))
        return ciphertext
    def decrypt(self, file_buffer):
        cleartext = self.__depad_file(self.__cipher.decrypt(file_buffer))
        return cleartext
    # Blowfish cipher needs 8 byte blocks to work with
    def __pad_file(self, file_buffer):
        pad_bytes = 8 - (len(file_buffer) % 8)                                 
        for i in range(pad_bytes - 1): file_buffer += chr(randrange(0, 256))
        # final padding byte; % by 8 to get the number of padding bytes
        bflag = randrange(6, 248); bflag -= bflag % 8 - pad_bytes
        file_buffer += chr(bflag)
        return file_buffer
    def __depad_file(self, file_buffer):
        pad_bytes = ord(file_buffer[-1]) % 8
        if not pad_bytes: pad_bytes = 8
        return file_buffer[:-pad_bytes]

if __name__ == '__main__':

    def print_usage():
        usage = "Usage: bfc -[e(encrypt) | d(decrypt) | c('cat' like)] infile [outfile]"
        print usage; sys.exit()

    def writefile(outfile_name, file_buffer):
        outfile = PrivoxyWindowOpen(outfile_name, 'wb')
        outfile.write(file_buffer)
        outfile.close()

    try: opts, args = getopt.getopt(sys.argv[1:], 'e:d:c:')
    except getopt.GetoptError: print_usage()

    opts = dict(opts)
    try: mode = opts.keys()[0]
    except IndexError: print_usage()

    ifname = opts[mode]

    try: ofname = args[0]
    except IndexError: ofname = ifname

    if os.path.exists(ifname):
        infile = PrivoxyWindowOpen(ifname, 'rb')
        filebuffer = infile.read()
        infile.close()
    else:
        print "file '%s' does not exist.\n" % ifname
        sys.exit()

    key = getpass()

    if mode == '-e':
        bfc = BFCipher(key); filebuffer = bfc.encrypt(filebuffer)
        writefile(ofname, filebuffer)
    elif mode == '-d':
        bfc = BFCipher(key); filebuffer = bfc.decrypt(filebuffer)
        writefile(ofname, filebuffer)
    elif mode == '-c':
        bfc = BFCipher(key); sys.stdout.write(bfc.decrypt(filebuffer))

    key = 'x'*len(key); del key
