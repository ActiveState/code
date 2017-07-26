void _Py_CountReferences(fp)
	FILE *fp;
{
	int n;
	PyObject *op;
	for (n = 0, op = refchain._ob_next;
	     op != &refchain;
	     op = op->_ob_next, n += op->ob_refcnt);
        fprintf(fp, "%d refs\n", n);
}

/* In my C extension, I put in the following macros. */

#if defined(Py_DEBUG) || defined(DEBUG)
extern void _Py_CountReferences(FILE*);
#define CURIOUS(x) { fprintf(stderr, __FILE__ ":%d ", __LINE__); x; }
#else
#define CURIOUS(x)
#endif
#define MARKER()        CURIOUS(fprintf(stderr, "\n"))
#define DESCRIBE(x)     CURIOUS(fprintf(stderr, "  " #x "=%d\n", x))
#define DESCRIBE_HEX(x) CURIOUS(fprintf(stderr, "  " #x "=%08x\n", x))
#define COUNTREFS()     CURIOUS(_Py_CountReferences(stderr))

/*
To debug, I rebuild Python using 'make OPT="-DPy_DEBUG"', which
causes the stuff under Py_TRACE_REFS to be built. My own makefile
uses the same trick, by including these lines:

debug:
        make clean; make OPT="-g -DPy_DEBUG" all
CFLAGS = $(OPT) -fpic -O2 -I/usr/local/include -I/usr/include/python1.5
*/
