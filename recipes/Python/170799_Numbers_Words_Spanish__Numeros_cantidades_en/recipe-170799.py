# num2pal version 1.0
#
# Números a palabras en Español.
# Autor:    Felipe Barousse    fbarouse@piensa.com
#
# De mis primeros programas en Python. Pero aun funciona
#
# El algoritmo es muy simple: 
# solo recibe un número entero y lo parte en grupos de tres, de ahi
# decide si son unidades, decenas, miles, etc.
#
# Ejemplo:    num2pal.main('45635')
# Regresará la cadena: 'Cuarenta y seis mil seis cientos treinta y cinco'
#
# Externamente habrá que agregar al resultado las unidades (Pesos, Dólares,
#   Litros, Kilos, etc. etc.)  si es que las hay.
#
# Si quieres que tambien traduzca a palabras, por ejemplo los centavos
# -o la parte fraccional- de una cantidad, solo llama a esta rutina
# dos veces, una para la parte entera y otra para la parte fraccional
#
# Previamente debiste haber separado lo que estan ANTES y DESPUES del
# punto decimal para tal efecto
#
# Copyright 2000-2001       Felipe Barousse Boué
#                           Bufete Consultor de Mexico - Piensa Technologies
#                           Ap. Cap. Polanco # 336
#                           Mexico D.F., 11550,  Mexico
#                           http://www.piensa.com/
#                           info@piensa.com
# LICENCIA DE USO:
# Este programa puede ser usado libremente bajo el esquema de la 
# licencia LGPL
#
# En otras palabras, solo deberás darme el credito correspondiente en tu
# documentación por el uso de esta rutina, aun cuando la modifiques,
# deberas mencionar que fué basado tu trabajo en ésta idea.
#
# NO HAY GARANTIA ALGUNA SOBRE ESTA RUTINA NI POR EL RESULTADO DEL USO 
# QUE SE LE DE
#
# Este programa es usado en sistemas hecho en Python para aplicaciones 
# de negocios,
# para imprimir facturas y recibos oficiales que requiren las cantidades en
# letra.
#
# Gracias!                       Felipe Barousse
#
# Creacion inicial:             5 de Febrero de 2000
# Ultima modificación:          26 Febrero 2001
#
#
def unidades(x):
    if x == 0:
        unidad = "cero"
    if x == 1:
        unidad = "un"
    if x == 2:
        unidad = "dos"
    if x == 3:
        unidad = "tres"
    if x == 4:
        unidad = "cuatro"
    if x == 5:
        unidad = "cinco"
    if x == 6:
        unidad = "seis"
    if x == 7:
        unidad = "siete"
    if x == 8:
        unidad = "ocho"
    if x == 9:
        unidad = "nueve"
    return unidad

def teens(x):
    if x == 0:
        teenname = "diez"
    if x == 1:
        teenname = "once"
    if x == 2:
        teenname = "doce"
    if x == 3:
        teenname = "trece"
    if x == 4:
        teenname = "catorce"
    if x == 5:
        teenname = "quince"
    return teenname


def tens(x):
    if x == 1:
        tensname = "diez"
    if x == 2:
        tensname = "veinte"
    if x == 3:
        tensname = "treinta"
    if x == 4:
        tensname = "cuarenta"
    if x == 5:
        tensname = "cincuenta"
    if x == 6:
        tensname = "sesenta"
    if x == 7:
        tensname = "setenta"
    if x == 8:
        tensname = "ochenta"
    if x == 9:
        tensname = "noventa"
    return tensname

def tercia(num):
    numero=str(num)
    if len(numero) == 1:
        numero='00'+numero
    if len(numero) == 2:
        numero='0'+numero
    a=int(numero[0])
    b=int(numero[1])
    c=int(numero[2])
#       print a, b, c
    if a == 0:
        if b == 0:
            resultado=unidades(c)
            return resultado
        elif b == 1:
            if c >= 0 and c <= 5:
                resultado = teens(c)
                return resultado
            elif c >= 6 and c <= 9:
                resultado = tens(b)+' y '+unidades(c)
                return resultado
        elif b == 2:
            if c == 0:
                resultado = 'veinte'
                return resultado
            elif c > 0 and c <= 9:
                resultado ='veinti '+unidades(c)
                return resultado
        elif b >=3 and b <= 9:
            if c == 0:
                resultado = tens(b)
                return resultado
            if c >= 1 and c <= 9:
                resultado = tens(b)+' y '+unidades(c)
                return resultado
    if a == 1:
        if b == 0:
            if c == 0:
                resultado = 'cien'
                return resultado
            elif c > 0 and c <= 9:
                resultado ='ciento '+unidades(c)
                return resultado
        elif  b == 1:
            if c >= 0 and c <= 5:
                resultado = 'ciento '+teens(c)
                return resultado
            elif c >= 6 and c <= 9:
                resultado = 'ciento '+tens(b)+' y '+unidades(c)
                return resultado
        elif b == 2:
            if c == 0:
                resultado = 'ciento veinte'
                return resultado
            elif c > 0 and c <= 9:
                resultado ='ciento veinti '+unidades(c)
                return resultado
        elif b >= 3 and b <= 9:
            if c == 0:
                resultado = 'ciento '+tens(b)
                return resultado
            elif c > 0 and c <= 9:
                resultado = 'ciento '+tens(b)+ ' y '+unidades(c
)
                return resultado

    elif a >= 2 and a <= 9:
        if a == 5:
            prefix='quinientos '
        elif a == 7:
            prefix='setecientos '
        elif a == 9:
            prefix='novecientos '
        else:
            prefix=unidades(a)+' cientos '
        if b == 0:
            if c == 0:
                resultado = prefix
                return resultado
            elif c > 0 and c <= 9:
                resultado = prefix+unidades(c)
                return resultado
        elif b == 1:
            if c >= 0 and c <= 5:
                resultado = prefix+teens(c)
                return resultado
            elif c >= 6 and c <= 9:
                resultado = prefix+tens(b)+' y '+unidades(c)
                return resultado
        elif b == 2:
            if c == 0:
                resultado = prefix+' veinte'
                return resultado
            elif c > 0 and c <= 9:
                resultado = prefix+' veinti '+unidades(c)
                return resultado
        elif b >= 3 and b <= 9:
            if c == 0:
                resultado = prefix+tens(b)
                return resultado
            elif c > 0 and c <= 9:
                resultado = prefix+tens(b)+' y '+unidades(c)
                return resultado
def main(num):
    result=''
    numero=str(num)
    if len(numero) == 1:
        numero='00000000'+numero
    if len(numero) == 2:
        numero='0000000'+numero
    if len(numero) == 3:
        numero='000000'+numero
    if len(numero) == 4:
        numero='00000'+numero
    if len(numero) == 5:
        numero='0000'+numero
    if len(numero) == 6:
        numero='000'+numero
    if len(numero) == 7:
        numero='00'+numero
    if len(numero) == 8:
        numero='0'+numero
    posicion=1
    for i in [0,3,6]:
        var=numero[i]+numero[i+1]+numero[i+2]
        if int(var) != 0:
            res=tercia(var)
            if i == 0:
                result=res+" millones "
            elif i == 3:
                result=result+res+" mil "
            elif i == 6:
                result=result+res
    return result 
