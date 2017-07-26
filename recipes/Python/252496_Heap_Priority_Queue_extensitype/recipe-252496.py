#include "Python.h"
#include "structmember.h"

/*   This is an example type extension.  This is based loosely on a data
 * structure described in 'Mastering Algorithms with C'.  It allocates memory
 * for the underlying array in "rows" instead of on an element-by-element
 * basis.  This does make it faster than the element-by-element allocating
 * version, but the difference is hard to measure until you get up into the
 * millions of elements.
 *
 *   This heap can be used with any Python object that implements a __cmp__
 * function.  I used the Python memory management functions and tried to make
 * this object blend in as much as possible to the Python framework.
 *
 *   Right now the only way to figure out how many items are on the hash is to
 * get the 'size' member of the hash (or keep count).
 */

/*----------------------------------------------------------------------------*
 *                               Heap structure                               *
 *----------------------------------------------------------------------------*/
typedef struct {
  PyObject_HEAD
  int size;        /* number of pointer elements held */
  int minsize;     /* minimum number of allocated elements in cache */
  int allocsize;   /* currently allocated size of cache */
  PyObject **tree; /* the cache */
} Heap;

/*----------------------------------------------------------------------------*
 *                                 Heap push                                  *
 *----------------------------------------------------------------------------*/
static PyObject *
Heap_push(PyObject *self, PyObject *arg)
{
  Heap *heap = (Heap *)self;
  PyObject **new_tree; /* new heap if needed */
  PyObject  *temp;     /* swap placeholder   */
  int cpos;            /* current position   */
  int ppos;            /* parent position    */
  int newsize;         /* size placeholder   */

  /* check to see if there is enough space allocated for the object */
  if (heap->size + 1 > heap->allocsize)
  {
    /* the size of the next row is always one plus the total size */
    newsize = 2*heap->allocsize + 1;

    /* allocate storage for the new node */
    new_tree = (PyObject **)PyMem_Realloc(heap->tree, newsize * sizeof(PyObject *));
    if (new_tree == NULL)
    {
      PyErr_SetString(PyExc_MemoryError, "unable to increase heap storage");
      return NULL;
    }
    else
      /* connect your new data structure and record the allocated size */
      heap->allocsize = newsize;
      heap->tree = new_tree;
  }

  /* insert the node after the last node */
  Py_INCREF(arg);
  heap->tree[heap->size] = arg;

  /* heapify the tree by pushing the contents of the new node upwards */
  cpos = heap->size;
  ppos = (cpos - 1)/2;

  while (cpos > 0 && PyObject_Compare(heap->tree[ppos], heap->tree[cpos]) < 0)
  {
    temp = heap->tree[ppos];
    heap->tree[ppos] = heap->tree[cpos];
    heap->tree[cpos] = temp;

    /* move up one layer in the tree and continue heapifying */
    cpos = ppos;
    ppos = (cpos - 1)/2;
  }

  /* adjust the size of the heap to account for the inserted data */
  heap->size++;
  Py_INCREF(Py_None);
  return Py_None;
}

/*----------------------------------------------------------------------------*
 *                                  Heap pop                                  *
 *----------------------------------------------------------------------------*/
static PyObject *
Heap_pop(PyObject *self)
{
  Heap *heap = (Heap *)self;
  PyObject **new_tree; /* new heap if needed */
  PyObject *data;      /* the top node       */
  PyObject *temp;      /* swap placeholder   */
  int ipos;            /* initial position   */
  int lpos;            /* left position      */
  int rpos;            /* right position     */
  int mpos;            /* modified position  */
  int newsize;         /* size placeholder   */

  /* do not allow extraction from an empty heap */
  if (heap->size == 0)
  {
    PyErr_SetString(PyExc_IndexError, "attempt to pop from empty heap");
    return NULL;
  }

  /* extract the first node, move the last node to the top of the heap */
  data = heap->tree[0];
  temp = heap->tree[heap->size - 1];
  heap->tree[0] = temp;

  /* check to see if you need to make the heap storage smaller */
  newsize = (heap->allocsize - 1)/2;
  if ((heap->size - 1 <= newsize) && (newsize >= heap->minsize))
  {
    new_tree = (PyObject **)PyMem_Realloc(heap->tree, newsize*sizeof(PyObject *));
    if (new_tree == NULL)
    {
      PyErr_SetString(PyExc_MemoryError, "unable to decrease heap storage");
      return NULL;
    }
    else
    {
      /* connect your new data structure and record the allocated size */
      heap->allocsize = newsize;
      heap->tree = new_tree;
    }
  }

  /* since you have pointers to the top and bottom nodes, decrease size */
  heap->size--;
  /* heapify the storage object by pushing the top node down */
  ipos = 0;

  while (1)
  {
    /* select the child to swap with the current node */
    lpos = ipos*2 + 1;
    rpos = ipos*2 + 2;

    if (lpos < heap->size && PyObject_Compare(heap->tree[lpos], heap->tree[ipos]) > 0)
      mpos = lpos;
    else
      mpos = ipos;

    if (rpos < heap->size && PyObject_Compare(heap->tree[rpos], heap->tree[mpos]) > 0)
      mpos = rpos;

    /* when mpos is ipos, the heap property has been restored */
    if (mpos == ipos)
      break;
    else
    {
      /* swap the contents of the current node and the selected child */
      temp = heap->tree[mpos];
      heap->tree[mpos] = heap->tree[ipos];
      heap->tree[ipos] = temp;
    }

    /* move down one level and continue heapifying */
    ipos = mpos;
  }

  return data;
}

/*----------------------------------------------------------------------------*
 *                              Heap destructor                               *
 *----------------------------------------------------------------------------*/
static void
Heap_dealloc(PyObject *self)
{
  int i;
  Heap *heap = (Heap *)self;

  /* remove references to everything on the heap */
  for ( i = 0; i < heap->size; i++ )
    Py_DECREF(heap->tree[i]);

  /* free the memory used by the pointers on the heap, if it exists */
  if (heap->tree != NULL)
    PyMem_Free(heap->tree);

  /* now free the type object */
  self->ob_type->tp_free(self);
}

/*----------------------------------------------------------------------------*
 *                              Heap constructor                              *
 *----------------------------------------------------------------------------*/
static PyObject *
Heap_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
  Heap *self;
  PyObject **tree;

  /* initialize an empty heap */
  self = (Heap *)type->tp_alloc(type, 0);
  self->size = 0;      /* number of currently held objects */
  self->minsize = 256; /* minimum number of allocated objects */
  tree = (PyObject **)PyMem_Malloc(self->minsize*sizeof(PyObject *));
  if (tree == NULL)
  {
    /* this is pretty much fatal - return an error and exit */
    PyErr_SetString(PyExc_MemoryError, "unable to allocate heap storage");
    self->allocsize = 0;
    return NULL;
  }
  else
  {
    /* return a new Heap */
    self->tree = tree;
    self->allocsize = self->minsize; 
    return (PyObject *)self;
  }
}

/*----------------------------------------------------------------------------*
 *                                Heap members                                *
 *----------------------------------------------------------------------------*/
static PyMemberDef Heap_members[] = {
  {"size", T_INT, offsetof(Heap, size), 0, "number of objects in the heap"},
  {NULL}  /* sentinel */
};

static PyMethodDef Heap_methods[] = {
  {"push", (PyCFunction)Heap_push, METH_O,      "push an object onto the heap"},
  {"pop",  (PyCFunction)Heap_pop,  METH_NOARGS, "pop the top object from the heap"},
  {NULL}  /* sentinel */
};

static PyTypeObject HeapType = {
  PyObject_HEAD_INIT(NULL)
  0,                         /* ob_size */
  "Heap",                    /* tp_name */
  sizeof(Heap),              /* tp_basicsize */
  0,                         /* tp_itemsize */
  (destructor)Heap_dealloc,  /* tp_dealloc */
  0,                         /* tp_print */
  0,                         /* tp_getattr */
  0,                         /* tp_setattr */
  0,                         /* tp_compare */
  0,                         /* tp_repr */
  0,                         /* tp_as_number */
  0,                         /* tp_as_sequence */
  0,                         /* tp_as_mapping */
  0,                         /* tp_hash  */
  0,                         /* tp_call */
  0,                         /* tp_str */
  0,                         /* tp_getattro*/
  0,                         /* tp_setattro*/
  0,                         /* tp_as_buffer*/
  Py_TPFLAGS_DEFAULT,        /* tp_flags*/
  "Heap objects",            /* tp_doc */
  0,                         /* tp_traverse */
  0,                         /* tp_clear */
  0,                         /* tp_richcompare */
  0,                         /* tp_weaklistoffset */
  0,                         /* tp_iter */
  0,                         /* tp_iternext */
  Heap_methods,              /* tp_methods */
  Heap_members,              /* tp_members */
  0,                         /* tp_getset */
  0,                         /* tp_base */
  0,                         /* tp_dict */
  0,                         /* tp_descr_get */
  0,                         /* tp_descr_set */
  0,                         /* tp_dictoffset */
  0,                         /* tp_init */
  0,                         /* tp_alloc */
  Heap_new,                  /* tp_new */
};

static PyMethodDef module_methods[] = {
  {NULL}  /* sentinel */
};

/* declarations for DLL export */
#ifndef PyMODINIT_FUNC
#define PyMODINIT_FUNC void
#endif
PyMODINIT_FUNC
initheap(void) 
{
  PyObject* m;

  if (PyType_Ready(&HeapType) < 0)
    return;

  m = Py_InitModule3("heap", module_methods, "Example module that implements a heap");

  if (m == NULL)
    return;

  Py_INCREF(&HeapType);
  PyModule_AddObject(m, "Heap", (PyObject *)&HeapType);
}
