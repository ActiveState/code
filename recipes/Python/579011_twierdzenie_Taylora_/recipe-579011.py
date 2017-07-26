#!/usr/bin/env python
#-*- coding: utf-8 -*-
import numpy as np
import pylab as py

def silnia(x):
    if x == 0:
        return 1
    else:
        return x * silnia(x-1)
        
def funkcja(n):
	f = (1.0/(silnia(n)))
	return float(f)
	
def szereg(n):
	a = 0 
	for i in range(n):
		a = a + funkcja(i)
	return a

def main():
	n = input("Podaj wyraz szeregu: ")
	print szereg(n)

main()

x = np.arange(0,20,1)
x = len(x)
y=[]
for i in range(x):
	y.append(szereg(i))
x = np.arange(0,20,1)
l1, = py.plot(x,y,'b', marker='o')
py.xlabel("numer wyrazu szeregu")
py.ylabel("wartosc wyrazu szeregu")
py.title("wykres")
py.savefig("wykres.png")
py.show()


def macierz():
	macierz = np.zeros((len(x),2))
	for j in range(len(x)):
		macierz[j,0]=x[j]
		macierz[j,1]=y[j]
	A = macierz
	np.savetxt("macierz.txt",A)

macierz()
