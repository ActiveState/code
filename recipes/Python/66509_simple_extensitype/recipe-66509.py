# copy these lines to a file named: setup.py
# To build and install the elemlist module you need the following
# setup.py file that uses the distutils:
from distutils.core import setup, Extension

setup (name = "elemlist",
       version = "1.0",
       maintainer = "Alex Martelli",
       maintainer_email = "aleax@aleax.it",
       description = "Sample Python module",

       ext_modules = [Extension('elemlist',sources=['elemlist.c'])]
)
# end of file: setup.py

/* copy these lines to a file named: elemlist.c */
/* and here comes elemlist.c itself with really minimal comments: */
#include "Python.h"

/* type-definition & utility-macros */
typedef struct {
    PyObject_HEAD
    PyObject *car, *cdr;
} cons_cell;
staticforward PyTypeObject cons_type;
/* a typetesting macro (we don't use it here) */
#define is_cons(v) ((v)->ob_type == &cons_type)
/* macros to access car & cdr, both as lvalues & rvalues */
#define carof(v) (((cons_cell*)(v))->car)
#define cdrof(v) (((cons_cell*)(v))->cdr)

/* ctor (factory-function) and dtor */
static cons_cell*
cons_new(PyObject *car, PyObject *cdr)
{
    cons_cell *cons = PyObject_NEW(cons_cell, &cons_type);
    if(cons) {
        cons->car = car; Py_INCREF(car);  /* INCREF when holding a PyObject* */
        cons->cdr = cdr; Py_INCREF(cdr);  /* ditto */
    }
    return cons;
}
static void
cons_dealloc(cons_cell* cons)
{
    /* DECREF when releasing previously-held PyObject*'s */
    Py_DECREF(carof(cons)); Py_DECREF(cdrof(cons));
    PyObject_DEL(cons);
}

/* Python type-object */
statichere PyTypeObject cons_type = {
    PyObject_HEAD_INIT(0)    /* initialize to 0 to ensure Win32 portability */
    0,                 /*ob_size*/
    "cons",            /*tp_name*/
    sizeof(cons_cell), /*tp_basicsize*/
    0,                 /*tp_itemsize*/
    /* methods */
    (destructor)cons_dealloc, /*tp_dealloc*/
    /* implied by ISO C: all zeros thereafter */
};

/* module-functions */
static PyObject*
cons(PyObject *self, PyObject *args)    /* the exposed factory-function */
{
    PyObject *car, *cdr;
    if(!PyArg_ParseTuple(args, "OO", &car, &cdr))
        return 0;
    return (PyObject*)cons_new(car, cdr);
}
static PyObject*
car(PyObject *self, PyObject *args)     /* car-accessor */
{
    PyObject *cons;
    if(!PyArg_ParseTuple(args, "O!", &cons_type, &cons))  /* type-checked */
        return 0;
    return Py_BuildValue("O", carof(cons));
}
static PyObject*
cdr(PyObject *self, PyObject *args)     /* cdr-accessor */
{
    PyObject *cons;
    if(!PyArg_ParseTuple(args, "O!", &cons_type, &cons))  /* type-checked */
        return 0;
    return Py_BuildValue("O", cdrof(cons));
}
static PyMethodDef elemlist_methods[] = {
    {"cons",   cons,   METH_VARARGS},
    {"car",    car,    METH_VARARGS},
    {"cdr",    cdr,    METH_VARARGS},
    {0, 0}
};

/* module entry-point (module-initialization) function */
void
initelemlist(void)
{
    /* Create the module and add the functions */
    PyObject *m = Py_InitModule("elemlist", elemlist_methods);
    /* Finish initializing the type-objects */
    cons_type.ob_type = &PyType_Type;
}

/* end of file: elemlist.c */
