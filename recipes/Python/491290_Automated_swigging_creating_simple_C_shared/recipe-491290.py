import commands


def swigit(modulename, Csources, Cheaders,
           SwigExtra ="",
           Libs = ['-lm'],
           PythonIncludePath='/usr/local/include/python2.4/',
           verbose=False):
    """
    Creates a shared C module for inclusion in Python.
    
    Arguments 
       modulename -  name of module to create (no extension).
       Cheaders   -  list of header files.
       Csources   -  list of source files.
       SwigExtra  -  additional swig declarations as a string.
       Libs       -  list of extra libs to link.
       PythonIncludePath - Python's include directory.
       verbose    -  set to True for informative message printing.

    In the current version, all header and source files are assumed to be
    in the current directory.
    """
    
    """
    1. Create the swig interface file modulename.i
    """
    s = ""
    s = "%module " + "%s\n" % modulename
    s = s + "%{\n"
    for header in Cheaders:
        s = s + '#include "%s"\n' % header
    s = s + "%}\n\n"

    # Modify recipe to handle particular cases.
    s = s + SwigExtra

    for header in Cheaders:
        s = s + "%%include %s \n" % header
    if verbose:
        print "Creating swig interface file with contents:\n", s
    str2file(s, "%s.i" % modulename)

    """
    2. Create the shared dll.
    """
    s = "swig -python %s.i" % modulename
    if verbose:
        print "Processing interface file:"
        print " ", s
    status, output = commands.getstatusoutput(s)
    if status != 0:
        if verbose:
            print output
        return status

    """
    3. Compile wrapper file.
    """
    s = "gcc -Wall -I%s -fpic -c %s_wrap.c" % (PythonIncludePath, modulename)
    status, output = commands.getstatusoutput(s)

    s = "gcc -Wall -fpic -c "
    for source in Csources:
        s = s + " %s " % source
    print "Compiling wrapper and source files to object files."
    print " ", s
    status, output = commands.getstatusoutput(s)
    if status != 0:
        if verbose:
            print output
        return status

    """
    4.  Create the shared module file.
    """
    s = "gcc -Wall -O3 "
    for lib in Libs:
        s = s + " %s "  % lib
    s = s + " -shared %s_wrap.o" % modulename
    for source in Csources:
        s = s + " %s.o" % source.split(".")[0]
    s = s + " -o _%s.so" % modulename
    if verbose:
        print "\nCreating module file."
        print " ", s
    status, output = commands.getstatusoutput(s)
    if status != 0:
        if verbose:
            print output
    return status

def str2file(s, filename):
    """
    Dumps string to file.
    """
    f = open(filename, "wt")
    for lines in s.split("\n"):
        print >> f, lines
    f.close()


if __name__ == "__main__":

    extra = """
%include "carrays.i"
%array_class(double, doubleArray)
%array_class(int, intArray)
"""

    modulename = "mymodule"
    if swigit(modulename, ["sphere.c"], ["sphere.h"], SwigExtra = extra, verbose=True) != 0:
        print "There is an error in processing ", modulename
    else:
        import mymodule
        
        x    = mymodule.doubleArray(2)
        x[0] = 2.0
        x[1] = 1.0

        print mymodule.sphere(2, x)
