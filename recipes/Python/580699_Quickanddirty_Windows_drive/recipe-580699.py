from __future__ import print_function

'''
Author: Vasudev Ram
Copyright 2016 Vasudev Ram
Web site: https://vasudevram.github.io
Blog: http://jugad2.blogspot.com
'''

from os.path import exists

def drives():
    # Limit of 'N' chosen arbitrarily.
    # For letters in the first half of the alphabet:
    for drive in range(ord('A'), ord('N')):
        print('Drive', chr(drive), 'exists:', exists(chr(drive) + ':'))

print()

drives()

print()

def drives2():
    drive_list = []
    for drive in range(ord('A'), ord('N')):
        if exists(chr(drive) + ':'):
            drive_list.append(chr(drive))
    return drive_list

print("The following drives exist:", drives2())
