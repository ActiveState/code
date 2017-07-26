#!/usr/bin/env python
#-*- coding: utf-8 -*-
import scipy.optimize as so
import scipy.integrate as si
import scipy.fftpack as ff
import numpy as np
import pylab as py


def func(t):
	f = np.exp(-t)*np.cos(20.0*np.pi*t)
	return f

def funkcja(t):
	f = np.exp(-t)*np.cos(20.0*np.pi*t)+0.5*np.exp(-t/0.5)*np.cos(10.0*np.pi*t)
	return f

x = np.arange(0.0,10.0,0.01)
y = func(x)
y1 = funkcja(x)

py.xlabel("t[s]")
py.ylabel("A(t)")
py.title("wykres")

z=ff.fft(y)
z1=ff.fft(y1)
widmo = np.abs(z[:len(z)/2])
widmo1 = np.abs(z1[:len(z1)/2])

py.subplot(4,1,1)
py.plot(x,y)

py.subplot(4,1,2)
py.plot(widmo)

py.subplot(4,1,3)
py.plot(x,y1)

py.subplot(4,1,4)
py.plot(widmo1)

py.savefig("wykres.png")
py.show()
