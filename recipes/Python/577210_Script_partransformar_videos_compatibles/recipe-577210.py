#!/usr/bin/env python 
# -*- coding: utf-8 -*-
#
#       avi2mp4.py
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
Script para transformar videos compatibles con reproductor MP4:
MP4 2GB FUJITEL 80MP4TV2 MP4-TV (AVIConverter_320X240_20FPS_EN Setup.exe)
Requiere:
    - ffmpeg - mencoder
Extras:
    Divide video en partes de 10 min
    Agrega subtítulos si existe el archivo file_name.srt
Uso:
    avi2mp4 file_name.avi
"""
import sys
import os
import getopt
import commands

# Variables
mp4dir = ''     # Directorio destino videos convertidos
                # por ejemplo /home/tu_usuario/mp4/
seg_part = 10 * 60      # Tamaño partes: 10 min = 600 seg

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
    basename, extension = os.path.splitext(arg)
    filename = os.path.basename(basename)
    ##print basename, extension, filename
    ##video_info = commands.getoutput('avidemux2_cli --nogui --load "%s" --autoindex --info --quit'%(arg)).split()
    video_info = commands.getoutput('ffmpeg -i "%s"'%(arg)).split() # Agrega "" para evitar
    try:                                                            # problema ruta con espacios
        # Cálculo duración del video, -1 Saca la coma final
        duracion = video_info[video_info.index('Duration:')+1][:-1]
    except ValueError:
        raise ValueError, "Imposible determinar duración video"
    hr, min, seg = duracion.split(':')
    ##print duracion
    seg_total = float(hr)*3600 + float(min)*60 + float(seg)
    ##print seg_total
    npart = int(seg_total / seg_part)   # Número de partes
    seg_part_final = seg_total - seg_part * npart   # Parte final tamaño restante
    ##print npart, seg_part_final
    is_ok = 0
    end_seg = str(seg_part)
    for i in range(npart+1):
        init_seg = str(i * seg_part)
        if is_ok != 0:  # Si hay un error al generar una parte del video
            break
        elif i == npart:  # Parte final
            end_seg = str(seg_part_final)
        ##print init_seg, end_seg, i
        is_ok = os.system('mencoder "%s" -really-quiet \
                          -oac copy \
                          -ovc xvid -xvidencopts bitrate=687 \
                          -ss %s -endpos %s \
                          -sub "%s.srt" \
                          -ofps 20 \
                          -vf scale=320:240 \
                          -o "%s%s-0%s.avi"'
                          %(arg, init_seg, end_seg, basename, mp4dir, filename, i))
    if is_ok == 0:
        print 'Conversión realizada con éxito!\nRevisar archivos en %s'%(mp4dir)
    else:
        print 'Conversión fallida!\nRevisar archivos en %s'%(mp4dir)

if __name__ == "__main__":
    main()
