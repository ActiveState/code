#!/usr/bin/env python 
# -*- coding: utf-8 -*-

# loop infinito
while True:
    # 1. Necesitamos leer la instrucción que el usuario quiere ejecutar, y la guardaremos en un string
    instruccion = raw_input("-->")

    # 1.1 Si la instrucción es Exit se sale del loop infinito
    if instruccion == 'Exit':
        break

    # 2. Evaluaremos el string ingresado en el paso 1. usando la función eval() vamos a almacenar el  resultado
    resultado = eval(instruccion)

    # 3. Mostraremos en pantalla el resultado obtenido en el paso 2.
    print(resultado)
