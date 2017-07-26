#!/usr/bin/env python 
# -*- coding: utf-8 -*-
#
#       aire.py
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
Script para saber calida del aire Santiago de Chile
    
"""
import urllib
import re

def extract_source():
    url = "http://www.seremisaludrm.cl/sitio/pag/aire/indexjs3aireindices-prueba.asp"
    sock = urllib.urlopen(url)
    htmlSource = sock.read()
    sock.close()
    return htmlSource

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

def extract_date(htmlSource):
    source = htmlSource[5974:5974+100] # Informacion
    return re.findall(r'\d+/\d+/\d+',htmlSource[5974:5974+100])[0]

def extract_time(htmlSource):
    source = htmlSource[5974:5974+100] # Informacion
    return re.findall(r'\d+:\d+',htmlSource[5974:5974+100])[0]

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    htmlSource = extract_source()
    date = extract_date(htmlSource)
    time = extract_time(htmlSource)
    print 'Calidad del aire en Santiago de Chile %s a las %s\n'%(date, time)
    data = extract_data(htmlSource)
    for i in data:
        print '\t\t'.join(i)
