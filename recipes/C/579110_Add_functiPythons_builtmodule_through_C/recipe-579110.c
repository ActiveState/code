#include <stdio.h>
#include <Python.h>

PyObject *pName, *pModule, *pFunc;
PyObject *builtin,  *builtinname, *builtin_dict, *myfunc;

/* python mymodule */
static PyObject*
mymodule_usleep(PyObject *self, PyObject *args)
{
    unsigned long  i;

    if (!PyArg_ParseTuple(args, "k:usleep", &i)) {
	return NULL;
    }
    usleep(i);

    return Py_None;
}

static char mymodule_usleep_doc[] =
    "usleep(unsigned long) - Sleep for the specified number of microseconds.";

static PyMethodDef mymodule_methods[] = {
    {"usleep",	mymodule_usleep,	METH_VARARGS,	mymodule_usleep_doc},
    {NULL, NULL}
};
/* python mymodule */

int
pyinit(char * pfile)
{
    char syspath[255], pwd[255];
    char fname[] = "bar";

    Py_Initialize();

    /* need for add pwd directory */
    PyRun_SimpleString("import sys");
    strcpy(syspath, "sys.path.append('");
        if (getcwd(pwd, sizeof(pwd)) != NULL) {
            strcat(syspath, pwd);
        }
    strcat(syspath, "')");

    PyRun_SimpleString(syspath);

    /* add new function to __builtin__ module  */
    // http://stackoverflow.com/questions/6565175/adding-new-command-to-module-through-c-api
    // Python3: https://mail.python.org/pipermail/python-list/2015-October/697917.html
    pName = PyString_FromString("__builtin__");
    builtin = PyImport_Import(pName);
    builtinname = PyString_FromString("__builtin__");
    
    builtin_dict = PyModule_GetDict(builtin);
    myfunc = PyCFunction_NewEx(&mymodule_methods[0], (PyObject*)NULL, builtinname);
    PyDict_SetItemString(builtin_dict, "usleep", myfunc);
    
    Py_DECREF(pName);
    /* end of new function adding */

    /* load Own python script */
    pName = PyString_FromString(pfile);
    PyErr_Print();

    pModule = PyImport_Import(pName);
    Py_DECREF(pName);

    if (pModule != NULL) {
        pFunc = PyObject_GetAttrString(pModule, fname);

        if (pFunc && PyCallable_Check(pFunc)) {
	    return 0;
        }
        else {
            if (PyErr_Occurred()) {
                PyErr_Print();
	    }
            fprintf(stderr, "Cannot find function \"%s\"\n", fname);
	    Py_XDECREF(pFunc);
	    Py_XDECREF(pModule);
	    Py_XDECREF(builtin);
	    Py_XDECREF(builtinname);
	    Py_XDECREF(builtin_dict);
	    Py_XDECREF(myfunc);
	    return 1;
        }
    }
    else {
        PyErr_Print();
        fprintf(stderr, "Failed to load \"%s\"\n", pfile);
        return 1;
    }
    return 0;
}

void myloop() {
    int rc, var1, var2;
    PyObject *mydict, *pArgs, *pValue;

    printf("Enter numbers:");
    rc = scanf("%d %d", &var1, &var2);
    while (rc == 2) {
	mydict = Py_BuildValue("{sisi}","a", var1, "b", var2);
	pArgs = PyTuple_New(1);
	PyTuple_SetItem(pArgs, 0, mydict);

	pValue = PyObject_CallObject(pFunc, pArgs);
	Py_DECREF(pArgs);
	if (pValue != NULL) {
	    printf("Result of call: %ld\n", PyInt_AsLong(pValue));
	    Py_DECREF(pValue);
	}
	else {
	    PyErr_Print();
	    fprintf(stderr,"Call failed\n");
	}
	Py_DECREF(mydict);
	printf("Enter numbers: ");
	rc = scanf("%d %d", &var1, &var2);
    }
}

int main(int argc, char **argv) {
    if (argc < 2) {
	fprintf(stderr, "Usage: call pythonfile\n");
	return 1;
    }
    if (pyinit(argv[1]) == 0) {
	myloop();
	Py_DECREF(pFunc);
	Py_DECREF(pModule);
	Py_DECREF(builtin);
	Py_DECREF(builtinname);
	Py_DECREF(builtin_dict);
	Py_DECREF(myfunc);
    }

    Py_Finalize();
    return 0;
}
