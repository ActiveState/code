#!/usr/bin/env python 
# -*- coding: utf-8 -*-
#
#       feedjit.py
#       
#       Copyright 2010 Javier Rovegno Campos <tatadeluxe<at>gmail.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#
"""
Script to extract data from feedjit
Example:
    # Options from command line
    $ python feedjit.py -o db.csv http://live.feedjit.com/live/XXXXXXXXXXXXXXXXXX/0/
    # If you have set Default vars inside the script, just run
    $ python feedjit.py
    
"""
import urllib
import sys
import os
import getopt
import json
import csv
import datetime

# Default vars
url_feedjit = 'http://live.feedjit.com/live/XXXXXXXXXXXXXXXXXXXXXX/0/'
csv_file = 'db.csv'

def main():
    global csv_file
    # Parse command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:", ["help", "output="])
    except getopt.error, msg:
        print msg
        print "for help use --help"
        sys.exit(2)
    # Process options
    for o, a in opts:
        if o in ("-h", "--help"):
            print __doc__
            sys.exit(0)
        if o in ("-o", '--output'):
            csv_file = a
    # Assign url
    if args == []:
        args = [url_feedjit]
    # Process arguments
    for arg in args:
        process(arg, csv_file) # process() is defined elsewhere


def process(arg, csv_file):
    '''
    >>> process('http://live.feedjit.com/live/XXXXXXXXXXXXXXXXXX/0/', 'test.csv')
    Traceback (most recent call last):
        ...
    ValueError: Data Download Failed!
    '''
    plain_data = extracts_data(arg)
    plain_text = latin2text(plain_data)
    json_data = json.loads(plain_text)
    first_row = None
    csv_exists = False
    if os.path.exists(csv_file):
        f_in = open(csv_file, "rb")
        Reader = csv.reader(f_in, dialect=csv.excel)
        encabezado = Reader.next()
        first_row = Reader.next()
        csv_exists = True 
    f_out = open(csv_file+'~', 'wb')
    Writer = csv.writer(f_out, dialect=csv.excel)
    Writer.writerow(['URL', 'CC', 'COUNTRY', 'CITY', 'OS', 'BROWSER', 'DATE TIME', 'IP'])
    for row in rows_data(json_data):
        if row != first_row:
            Writer.writerow(row)
        else:
            Writer.writerow(first_row)
            for row_old in Reader:
                Writer.writerow(row_old)
            break
    f_out.close()
    if csv_exists:
        f_in.close()
        os.remove(csv_file)
    os.rename(csv_file+'~', csv_file)

def rows_data(json_data):
    key_list = [u'pgUrl', u'cc', u'cn', u'ln']
    for o in json_data:
        row = encode_list([o[x] for x in key_list])
        row.append(switchOS(o[u'uaos']))
        row.append(switchBrowser(o[u'uav']))
        row.append(switchDate(o[u'ct']))
        row.append(o[u'cip'])
        yield row

def extracts_data(url):
    sock = urllib.urlopen(url)
    htmlSource = sock.read()
    sock.close()
    try:
        # Try to find the data init block
        data_init = htmlSource.index('[{')
    except ValueError:
        raise ValueError, "Data Download Failed!"
    data_end = htmlSource.index('}]',data_init) + 2
    data_source = htmlSource[data_init:data_end]
    return data_source

def latin2text(word):
    dict_hex = {'&#xE1;': 'á',
                '&#xE9;': 'é',
                '&#xED;': 'í',
                '&#xF1;': 'ñ',
                '&#xF3;': 'ó',
                '&#xFA;': 'ú',
                '&#xFC;': 'ü'
                }
    for key in dict_hex.keys():
        word = word.replace(key,dict_hex[key])
    return word
    
def encode_list(words):
    aux = []
    for word in words:
        aux.append(word.encode("utf-8"))
    return aux
    
def switchOS(num):
    if int(num) == 1:
        return 'win98'
    elif int(num) == 2:
        return 'winxp'
    elif int(num) == 3:
        return 'winvista'
    elif int(num) == 5:
        return 'winxp'
    elif int(num) == 6:
        return 'linux'
    elif int(num) == 9:
        return 'win7'
    else:
        return 'unknown'

def switchBrowser(num):
    if int(num) == 1:
        return 'ie'
    elif int(num) == 2:
        return 'firefox'
    elif int(num) == 3:
        return 'safari'
    elif int(num) == 4:
        return 'opera'
    elif int(num) == 11:
        return 'chrome'
    else:
        return 'other'
        
def switchDate(num):
    date = datetime.datetime.fromtimestamp(float(num))
    return date.strftime("%d/%m/%Y %H:%M")
        
if __name__ == '__main__':
    import doctest
    doctest.testmod()
    main()
