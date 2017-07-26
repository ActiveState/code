#include "python.h"

extern void qsort(void *, size_t, size_t, int (*)(const void *, const void *));

static PyObject *py_compare_func = NULL;

static int
stub_compare_func(const PyObject **a, const PyObject **b)
{
    int retvalue = 0;

    // Build up the argument list... 
    PyObject *arglist = Py_BuildValue("(OO)", *a, *b);

    // ...for calling the Python compare function.
    PyObject *result = PyEval_CallObject(py_compare_func,arglist);

    if (result && PyInt_Check(result)) {
        retvalue = PyInt_AsLong(result);
    }

    Py_XDECREF(result);
    Py_DECREF(arglist);
    
    return retvalue;
}


static PyObject *pyqsort(PyObject *obj, PyObject *args)
{
    PyObject *pycompobj;
    PyObject *list;
    if (!PyArg_ParseTuple(args, "OO", &list, &pycompobj)) 
        return NULL;
    
    // make sure second argument is a function
    if (!PyCallable_Check(pycompobj)) {
        PyErr_SetString(PyExc_TypeError, "Need a callable object!");
    }
    else {
        // save the compare func. This obviously won't work for multi-threaded
        // programs.
        py_compare_func = pycompobj;
        if (PyList_Check(list)) {
            int size = PyList_Size(list);
            int i;
            
            // make an array of (PyObject *), because qsort does not know about
            // the PyList object
            PyObject **v = (PyObject **) malloc( sizeof(PyObject *) * size );
            for (i=0; i<size; ++i) {
                v[i] = PyList_GetItem(list, i);
                // increment the reference count, because setting the list items below
                // will decrement the ref count
                Py_INCREF(v[i]);
            }
            qsort(v, size, sizeof(PyObject*), stub_compare_func);
            for (i=0; i<size; ++i) {
                PyList_SetItem(list, i, v[i]);
                // need not do Py_DECREF - see above
            }
            free(v);
        }
    }
    Py_INCREF(Py_None);
    return Py_None;
}

static PyMethodDef qsortMethods[] = {
    { "qsort", pyqsort, METH_VARARGS },
    { NULL, NULL }
};

__declspec(dllexport) void initqsort(void) {
    PyObject *m;
    m = Py_InitModule("qsort", qsortMethods);
}


In Python
ActivePython 2.1, build 210 ActiveState)
based on Python 2.1 (#15, Apr 23 2001, 18:00:35) [MSC 32 bit (Intel)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import qsort
>>> a = [9, 3, 5, 4, 1]
>>> def revcmp(a, b): return cmp(b, a)
...
>>> qsort.qsort(a, revcmp)
>>> a
[9, 5, 4, 3, 1]
>>>
