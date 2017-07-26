from java import io
def saveObject(x,fname="jython.bin"):
    outs=io.ObjectOutputStream(io.FileOutputStream(fname))
    outs.writeObject(x)
    outs.close()
def loadObject(fname="jython.bin"):
    ins=io.ObjectInputStream(io.FileInputStream(fname))
    x=ins.readObject()
    ins.close()
    return x


x={1:1,'two':"2",'three':[1,2,3]}
saveObject(x)
y=loadObject()
print y
