#include <Python.h>

static PyObject* Foo_init(PyObject *self, PyObject *args)
{
    printf("Foo.__init__ called\n");
    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject* Foo_doSomething(PyObject *self, PyObject *args)
{
    printf("Foo.doSomething called\n");
    Py_INCREF(Py_None);
    return Py_None;
}

static PyMethodDef FooMethods[] = 
{
    {"__init__", Foo_init, METH_VARARGS, 
	 "doc string"},
    {"doSomething", Foo_doSomething, METH_VARARGS,
	 "doc string"},
    {NULL},
};

static PyMethodDef ModuleMethods[] = { {NULL} };

#ifdef __cplusplus
extern "C"
#endif
void initFoo()
{
    PyMethodDef *def;

    /* create a new module and class */
    PyObject *module = Py_InitModule("Foo", ModuleMethods);
    PyObject *moduleDict = PyModule_GetDict(module);
    PyObject *classDict = PyDict_New();
    PyObject *className = PyString_FromString("Foo");
    PyObject *fooClass = PyClass_New(NULL, classDict, className);
    PyDict_SetItemString(moduleDict, "Foo", fooClass);
    Py_DECREF(classDict);
    Py_DECREF(className);
    Py_DECREF(fooClass);
    
    /* add methods to class */
    for (def = FooMethods; def->ml_name != NULL; def++) {
	PyObject *func = PyCFunction_New(def, NULL);
	PyObject *method = PyMethod_New(func, NULL, fooClass);
	PyDict_SetItemString(classDict, def->ml_name, method);
	Py_DECREF(func);
	Py_DECREF(method);
    }
}
