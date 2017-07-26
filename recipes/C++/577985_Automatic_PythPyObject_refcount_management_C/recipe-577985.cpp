/*
 * auto_pyptr.h
 *
 * Originally from
 * http://code.activestate.com/recipes/528875-automatic-ref-count-management-in-c-using-a-smart-/
 */

#ifndef AUTO_PYPTR_H_
#define AUTO_PYPTR_H_

#include <Python.h>
#include <memory>

typedef std::auto_ptr<PyObject> auto_pyptr_base;

/**
 * An auto_ptr that, instead of deleting, decrements the reference count
 * of a PyObject pointer.
 *
 * Make sure to only use this when you get a *new* reference (Py_INCREF or
 * getting the result of any function that says it returns a new reference
 * to a PyObject), NOT for "borrowed" references.
 */
class auto_pyptr : public auto_pyptr_base {
public:
    auto_pyptr(PyObject * obj = NULL) : auto_pyptr_base(obj) {
    }
    ~auto_pyptr() {
        reset();
    }
    void reset(PyObject * obj = NULL) {
        if(obj != get()) {
            PyObject * old = release(); // Avoid the delete call
            Py_XDECREF(old);
            auto_pyptr_base::reset(obj);
        }
    }
    void inc() {
        PyObject * ptr = get();
        if(ptr)
            Py_INCREF(ptr);
    }

    /*
     * Implement cast to PyObject pointer so you don't have to call var.get()
     * every time you use the object.
     *
     * You still have to use get() in certain cases, notably varargs
     * (i.e. "..."). GCC will warn you that this will abort at runtime.
     */
    operator PyObject*() {
        return this->get();
    }
};

#endif /* AUTO_PYPTR_H_ */
