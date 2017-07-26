def whoaminow():
    "returns name of called calling function"
    import sys, dis

    # get frame where calling function is called
    frame = sys._getframe(2)

    # get code and next to last instruction from frame
    code = frame.f_code
    lasti = frame.f_lasti-3

    # redirect ouput of disassemble (stdout)
    oldout = sys.stdout
    sys.stdout = open('log','w')
    dis.disassemble(code, lasti)
    sys.stdout.close()
    sys.stdout = oldout  # restore stdout

    # retrieve current byte code line
    fd = open('log')
    for line in fd.xreadlines():
        if line.startswith('-->'):
            break
    else: # couldn't find name
        line = None
    fd.close()
    
    # isolate function name
    if line is not None:
        funcname = line.split()[-1][1:-1]
    else: 
        funcname = None
    return funcname





# some testing...        
def foo():
    me = whoaminow() 
    return me


bar = foo
baz = foo
print "%s %s %s"%(foo(), bar(), baz())


class c:
    def fro(self):
        return whoaminow()

inst = c()
bozz = inst.fro
print "%s %s"%(inst.fro(),bozz())

fl = [foo]
print fl[0]()

"""
OUTPUTS:
foo bar baz
fro bozz
None
"""
