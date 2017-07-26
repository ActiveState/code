#!/usr/bin/env python 
# -*- coding: utf-8 -*-
#
#       cvh_video.py
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
Script para descargar videos desde http://www.chilevision.cl/
Requiere:
    - aria2c - wget
Extras:
    Ofrece Descargar el resto de los videos
Uso:
    # Comillas requeridas, problema parser
    cvh_video.py "http://www.chilevision.cl/home/index.php?option=com_content&task=view&id=YYYYY&Itemid=XXX"
    
"""
import urllib
import re
import sys
import os
import getopt
import commands
import signal

def main():
    # parse command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
    except getopt.error, msg:
        print msg
        print "for help use --help"
        sys.exit(2)
    # process options
    for o, a in opts:
        if o in ("-h", "--help"):
            print __doc__
            sys.exit(0)
    # process arguments
    for arg in args:
        process(arg) # process() is defined elsewhere


def process(arg):
    '''
    >>> process('http://www.chilevision.cl/home/index.php?option=com_content&task=view&id=YYYYY&Itemid=XXX')
    Traceback (most recent call last):
        ...
    ValueError: Descarga video fallida, url no contiene video
    '''
    url_file = extrae_url_file(arg)
    is_ok = os.system('aria2c "%s"'%url_file)
    if is_ok == 0:
        print 'Descarga video realizada con éxito!'
        log_file(url_file)
        if pregunta_download_more():
            download_more(url_file)
        else:
            print 'La opción que elige es no descargar videos similares'
    elif is_ok == 32512:
        print 'Recomendamos que instale aria2c para acelerar la descarga'
        is_ok = os.system('wget "%s"'%url_file)
        log_file(url_file)
    else:
        print 'Descarga video fallida!'
        
def pregunta_download_more():
    return raw_input_timer('Descargar el resto de los videos similares s/(n): ',5) == 's\n'
        
def download_more(url_file):
    nn = ['01','02','03','04','05','06','07','08','09']
    for i in xrange(10,50):
        nn.append(str(i))
    ext = url_file[-4:]
    pref = url_file[:-6]
    errores = 0
    video_url_files = ''
    for n in nn:
        url_file_aux = '%s%s%s '%(pref,n,ext)
        if verifica_url_file(url_file_aux):
            log_file(url_file_aux)
            video_url_files += '%s '%(url_file_aux)
        elif errores <= 3:
            #Tolera hasta 3 errores
            errores += 1
        else:
            break
    if video_url_files != '':
        is_ok = os.system('aria2c -Z %s'%video_url_files)
    else:
        print "No hay más videos similares para descargar"

def verifica_url_file(url_file_aux):
    return urllib.urlopen(url_file_aux).info().typeheader == 'application/octet-stream'

def extrae_url_file(url):
    sock = urllib.urlopen(url)
    htmlSource = sock.read()
    sock.close()
    try:
        #Trata de buscar inicio url con video
        video_url_init = htmlSource.index('playerCHV(') + 11
    except ValueError:
        #Busca los enlaces hacia url con videos
        coleccion = re.findall("\d{,8}&Itemid=2389", htmlSource)
        video_url_list = ''
        for id in coleccion:
            #Agrega los id en una lista con los enlaces
            video_url_list += ('"http://www.chilevision.cl/home/index.php?option=com_content&task=view&id=%s&Itemid=2389" '
                               %id[:-12])
        if video_url_list != '':
            #Si encuentra alguna enlace hacia video válido los imprime en pantalla
            print video_url_list
            sys.exit(0)
        else:
            #No encuentra url con videos
            raise ValueError, "Descarga video fallida, url no contiene video"
    video_url_end = htmlSource.index('\'',video_url_init)
    video_url = htmlSource[video_url_init:video_url_end]
    video_url = video_url.replace('%2F','/')
    return video_url
    
def log_file(url_file):
    #Añade enlaces con videos descargados
    log = open('log_chv_video.txt', 'a')
    log.write("%s\n"%url_file)
    log.close()

def alarm_handler(*args):
    raise Exception("timeout")


#  
#  name: raw_input_timer
#  @param str solicita dato,int seg
#  @return texto
def raw_input_timer(prompt, timeout):
    signal.signal(signal.SIGALRM, alarm_handler)
    signal.alarm(timeout)
    sys.stdout.write(prompt)
    sys.stdout.flush()
    try:
        text = sys.stdin.readline()
    except:
        text = ""
    signal.alarm(0)
    return text

        
if __name__ == '__main__':
    import doctest
    doctest.testmod()
    main()
