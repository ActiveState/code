//----------------------------------------------------------------------------
// Return set(dict.keys()).issubset(set([vkeys, ...])
// keys of dict must be string or unicode in Py2 and string in Py3!
// Parameters:
// dict - the Python dictionary object to be checked
// vkeys - a null-terminated list of keys (char *)
//----------------------------------------------------------------------------
int checkDictKeys(PyObject *dict, const char *vkeys, ...)
{
    int i, j, rc;
    PyObject *dkeys = PyDict_Keys(dict);              // = dict.keys()
    if (!dkeys) return 0;                             // no valid dictionary
    j = PySequence_Size(dkeys);                       // len(dict.keys())
    PyObject *validkeys = PyList_New(0);              // make list of valid keys
    va_list ap;                                       // def var arg list
    va_start(ap, vkeys);                              // start of args
    while (vkeys != 0)                                // reached end yet?
        { // build list of valid keys to check against
#if PY_MAJOR_VERSION < 3
        PyList_Append(validkeys, PyBytes_FromString(vkeys));    // Python 2
#else
        PyList_Append(validkeys, PyUnicode_FromString(vkeys));  // python 3
#endif
        vkeys = va_arg(ap, const char *);             // get next char string
        }
    va_end(ap);                                       // end the var args loop
    rc = 1;                                           // prepare for success
    for (i = 0; i < j; i++)
    {   // loop through dictionary keys
        if (!PySequence_Contains(validkeys, PySequence_GetItem(dkeys, i)))
            {
            rc = 0;
            break;
            }
    }
    Py_DECREF(validkeys);
    Py_DECREF(dkeys);
    return rc;
}
