/* suppose we need an empty C-coded function, equivalent to Python:
def empty1(*args):
    pass
or identically:
def empty2(*args):
    return None
There is still a right and a wrong way to do it...!
*/

/* WRONG! will mess up reference counts...: */
static PyObject*
empty3(PyObject* self, PyObject* args)
{
    return Py_None;
}

/* Fine! the simplest way to do it...: */
static PyObject*
empty4(PyObject* self, PyObject* args)
{
    return Py_BuildValue("");
}

/* Fine! the canonical approach...: */
static PyObject*
empty5(PyObject* self, PyObject* args)
{
    Py_INCREF(Py_None);
    return Py_None;
}
