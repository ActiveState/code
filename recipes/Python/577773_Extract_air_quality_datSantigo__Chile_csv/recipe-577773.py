#!/usr/bin/env python 
# -*- coding: utf-8 -*-
#
#       aire-csv.py
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
'''
Usage: aire-csv.py [options] arg

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -f FILE, --file=FILE  sensors FILE database
'''
import os
import csv
import re
import urllib
from optparse import OptionParser

def main():
    usage = "usage: %prog [options] arg"
    version = "%prog 1.0"
    parser = OptionParser(usage=usage, version=version)
    parser.add_option("-f", "--file", dest="csv_file",
                  help="csv FILE database", metavar="FILE",
                  default='db-aire.csv')
    (options, args) = parser.parse_args()
    # Run the program
    process(options, args)

def process(options, args):
    '''
    Save air quality data in a csv_file
    '''
    url = "http://www.seremisaludrm.cl/sitio/pag/aire/indexjs3aireindices-prueba.asp"
    sock = urllib.urlopen(url)
    htmlSource = sock.read()
    sock.close()
    csv_file = options.csv_file
    csv_exists = False
    # Append sensors data
    air_data = extract_data(htmlSource)
    encabezado = air_data.next()
    encabezado.append('DATE')
    encabezado.append('TIME')
    date = extract_date(htmlSource)
    time = extract_time(htmlSource)
    if os.path.exists(csv_file):
        f_in = open(csv_file, "rb")
        Reader = csv.reader(f_in, dialect=csv.excel)
        encabezado_old = Reader.next()
        csv_exists = True
    f_out = open(csv_file+'~', 'wb')
    Writer = csv.writer(f_out, dialect=csv.excel)
    # TODO check encabezado == encabezado_old
    Writer.writerow(encabezado)
    for row in air_data:
        row.append(date)
        row.append(time)
        Writer.writerow(row)
    if csv_exists:
        for row in Reader:
            Writer.writerow(row)
        f_in.close()
        os.remove(csv_file)
    f_out.close()
    os.rename(csv_file+'~', csv_file)

def extract_date(htmlSource):
    source = htmlSource[5974:5974+100] # Informacion
    return re.findall(r'\d+/\d+/\d+',htmlSource[5974:5974+100])[0]

def extract_time(htmlSource):
    source = htmlSource[5974:5974+100] # Informacion
    return re.findall(r'\d+:\d+',htmlSource[5974:5974+100])[0]

def extract_data(htmlSource):
    source = htmlSource[6644:12988] # Tabla con informacion
    soup_data = re.findall(r'(?:<span\s.*">)(.*)(?:</span>)',source)
    j = 0
    row = []
    for element in soup_data:
        if j == 0:
            element = element.replace('&nbsp;',' ')
        if j == 2:
            element = element.replace('<br>',' ')
            element = element.replace(' ','')
        if j == 3:
            element = element.replace('<br>',' ')
            element = element.replace(' ','')
            row.append(element)
            j = 0
            aux = row
            row = []
            yield aux
        else:
            row.append(element)
            j += 1

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    main()
