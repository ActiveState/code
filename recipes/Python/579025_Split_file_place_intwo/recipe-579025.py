#! /usr/bin/python2

import os, sys
import argparse
import re

exit = sys.exit

size_pat = re.compile(r"^\d+[KMG]?$")
KBYTE = 1024
MBYTE = KBYTE * KBYTE
GBYTE = KBYTE * MBYTE
buf_size = 32768

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs=1, help="path to file name")
    parser.add_argument("-s", "--size", nargs=1, required=True, help="file is truncated to size")
    return parser.parse_args()

def truncate_to_size(fpath, truncated_size):
    with open(fpath, "ab") as F:
        return F.truncate(truncated_size)

def file_exists(fpath):
    return os.path.exists(fpath)

def get_file_size(fpath):
    return os.path.getsize(fpath)

def str_to_number(str_size):
    if str_size[-1].isdigit():
        return int(str_size)
    num, unit = int(str_size[:-1]), str_size[-1:]
    if unit == 'K':
        num *= KBYTE
    elif unit == 'M':
        num *= MBYTE
    elif unit == 'G':
        num *= GBYTE
    return num

def copy_segment_to_file(in_fpath, start, end, out_fpath):
    if start >= end:
        return
    outfile = open(out_fpath, "wb")
    infile = open(in_fpath, "rb")
    infile.seek(start, 0)
    data = ''
    while start < end:
        data = infile.read(buf_size)
        if data == '':
            break
        start += len(data)
        outfile.write(data)
    infile.close()
    outfile.close()

if __name__ == '__main__':
    args = parse_args()
    fpath = args.file[0]
    fstr_size = args.size[0]
    if not size_pat.search(fstr_size):
        print("ERROR: invalid size")
        exit(1)
    if not file_exists(fpath):
        print("ERROR: file doesn't exist")
        exit(1)
    fsize = get_file_size(fpath)
    trunc_size = str_to_number(fstr_size)
#    print "fsize", fsize
#    print "fsize", trunc_size
    if trunc_size > fsize:
        print("WARN: truncated size must be less than or equal to file size.")
        exit(1)
    copy_segment_to_file(fpath, trunc_size, fsize, fpath+"_part2")
    truncate_to_size(fpath, trunc_size)
