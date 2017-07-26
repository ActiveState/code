/** START - First code written in C (calc.c). **/
/**
 *  A simple calculator that works with whole numbers written in C.
 *  Copyright (C) 2008 by Nycholas de Oliveira e Oliveira <nycholas@gmail.com>
 *
 *  This program is free software; you can redistribute it and/or
 *  modify it under the terms of the GNU General Public License
 *  as published by the Free Software Foundation; either version 2
 *  of the License, or (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
 *  MA  02110-1301, USA.
 */

#include <stdlib.h>
#include <stdio.h>

int calc_sum(int, int);
int calc_subtract(int, int);
int calc_multiplies(int, int);
int calc_divides(int, int);

int main(void) {
    int a = 6;
    int b = 2;
    printf(" a = %d; b = %d;\n", a, b);
    printf("==============\n\n");
    printf(" + sum: %d\n", calc_sum(a, b));
    printf(" + subtract: %d\n", calc_subtract(a, b));
    printf(" + multiplies: %d\n", calc_multiplies(a, b));
    printf(" + divides: %d\n", calc_divides(a, b));
    return 0;
}

int calc_sum(int a, int b) {
    return a + b;
}

int calc_subtract(int a, int b) {
    return a - b;
}

int calc_multiplies(int a, int b) {
    return a * b;
}

int calc_divides(int a, int b) {
    return a / b;
}
/** END - First code written in C (calc.c). **/

/** START - According code written in C / Python (pycalc.c). **/
/**
 *  A simple calculator that works with whole numbers written in C/Python.
 *  Copyright (C) 2008 by Nycholas de Oliveira e Oliveira <nycholas@gmail.com>
 *
 *  This program is free software; you can redistribute it and/or
 *  modify it under the terms of the GNU General Public License
 *  as published by the Free Software Foundation; either version 2
 *  of the License, or (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
 *  MA  02110-1301, USA.
 */

#include <stdlib.h>
#include <python2.5/Python.h>

static PyObject *pycalc_sum(PyObject *self, PyObject *args) {
    int a, b;
    if (!PyArg_ParseTuple(args, "ii", &a, &b))
        return NULL;
    return Py_BuildValue("i", (a + b));
}

static PyObject *pycalc_subtract(PyObject *self, PyObject *args) {
    int a, b;
    if (!PyArg_ParseTuple(args, "ii", &a, &b))
        return NULL;
    return Py_BuildValue("i", (a - b));
}

static PyObject *pycalc_multiplies(PyObject *self, PyObject *args) {
    int a, b;
    if (!PyArg_ParseTuple(args, "ii", &a, &b))
        return NULL;
    return Py_BuildValue("i", (a * b));
}

static PyObject *pycalc_divides(PyObject *self, PyObject *args) {
    int a, b;
    if (!PyArg_ParseTuple(args, "ii", &a, &b))
        return NULL;
    return Py_BuildValue("i", (a / b));
}

static PyMethodDef pycalc_methods[] = {
    {"sum", pycalc_sum, METH_VARARGS, "Sum two integers."},
    {"subtract", pycalc_subtract, METH_VARARGS, "Subtracts two integers."},
    {"multiplies", pycalc_multiplies, METH_VARARGS, "Subtracts two integers."},
    {"divides", pycalc_divides, METH_VARARGS, "Divide two integers."},
    {NULL, NULL, 0, NULL}
};

void initpycalc(void) {
    PyObject *m;
    m = Py_InitModule("pycalc", pycalc_methods);
    if (m == NULL)
        return;
}

int main(int argc, char *argv[]) {
    Py_SetProgramName(argv[0]);
    Py_Initialize();
    initpycalc();
    return 0;
}
/** END - According code written in C / Python (pycalc.c). **/

## START - Code setup.py. ##
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   Script `setup` the install/build Simple calculator.
#   Copyright (C) 2008 by Nycholas de Oliveira e Oliveira <nycholas@gmail.com>
#
#   This program is free software; you can redistribute it and/or
#   modify it under the terms of the GNU General Public License
#   as published by the Free Software Foundation; either version 2
#   of the License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#   MA  02110-1301, USA.
#
"""A simple calculator that works with whole numbers written in C / Python."""

from distutils.core import setup, Extension

def run():
    setup(name='pycalc',
          version='0.1',
          author='Nycholas de Oliveira e Oliveira',
          author_email='nycholas@gmail.com',
          license='GNU General Public License (GPL)',
          description="""A simple calculator that works with """
                      """whole numbers written in C/Python.""",
          platforms=['Many'],
          ext_modules=[Extension('pycalc', sources = ['pycalc.c'])]
    )

# Commands:
#
# ++ clean up temporary files from 'build' command
# ./setup.py clean -a
#
# ++ build everything needed to install
# ./setup.py build
#
# ++ install everything from build directory
# ./setup.py install -c -O2
#

if __name__ == "__main__":
    run()
## END - Code setup.py. ##
