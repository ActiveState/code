#!/usr/bin/env python 
# -*- coding: utf-8 -*-
#
#       zigzag.py
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

def zigzag(n):
    # Genera la matriz n x n rellena con 'x'
    aux = [['x' for x in range(n)] for y in range(n)]
    i = 0
    j = 0
    der = True
    abajo = False
    izq_abajo = False
    der_arriba = False
    for k in range(n**2):
        aux[i][j] = k
        if der:
            j += 1
            der = False
            if i == 0:
                izq_abajo = True
            if i == n - 1:
                der_arriba = True
            continue
        if abajo:
            i += 1
            abajo = False
            if j == 0:
                der_arriba = True
            if j == n - 1:
                izq_abajo = True
            continue
        if izq_abajo:
            j -= 1
            i += 1
            if i == n - 1:
                izq_abajo = False
                der = True
            elif j == 0:
                izq_abajo = False
                abajo = True
            continue
        if der_arriba:
            j += 1
            i -= 1
            if j == n - 1:
                der_arriba = False
                abajo = True
            elif i == 0:
                der_arriba = False
                der = True
            continue
    return aux

if __name__ == '__main__':
    for n in range(1,15):
        lnds = zigzag(n)
        print 'Caso N = %s' % n
        for row in lnds:
            print row
