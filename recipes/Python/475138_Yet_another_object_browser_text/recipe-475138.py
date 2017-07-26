class ObjectDescender:
    def __init__(self, maxdepth, outf=sys.stderr):
        self.already = [ ]
        self.maxdepth = maxdepth
        self.outf = outf

    def exclude(self, attr, obj):
        return False
    def showThis(self, attr, obj):
        return True

    def prefix(self, depth, pn):
        return ((depth * "\t") + ".".join(pn) + ": ")

    def handleLeaf(self, v, depth, pn):
        def trepr(v):
            if v == None:
                return "None"
            elif type(v) == types.InstanceType:
                r = v.__class__.__name__
            else:
                r = repr(type(v))
            return "%s at %x" % (r, id(v))
        if type(v) in (types.ListType, types.TupleType):
            self.outf.write(self.prefix(depth, pn) + trepr(v))
            if len(v) == 0:
                self.outf.write(" (empty)")
            self.outf.write("\n")
        elif type(v) in (types.StringType, types.IntType,
                         types.FloatType, types.ComplexType):
            self.outf.write(self.prefix(depth, pn) + repr(v) + "\n")
        else:
            self.outf.write(self.prefix(depth, pn) + trepr(v) + "\n")

    def getAttributes(self, obj):
        lst = dir(obj)
        if hasattr(obj, "__dict__"):
            for x in obj.__dict__.keys():
                if x not in lst:
                    lst.append(x)
        lst.sort()
        def filt(x):
            return x not in ("__doc__",)
        return filter(filt, lst)

    def descend(self, obj, depth=0, pathname=[ ]):
        if obj in self.already:
            return
        self.already.append(obj)
        if depth == 0:
            self.handleLeaf(obj, depth, pathname)
        if depth >= self.maxdepth:
            return
        if type(obj) in (types.ListType, types.TupleType):
            lst = [ ]
            if len(pathname) > 0:
                lastitem = pathname[-1]
                pathname = pathname[:-1]
            else:
                lastitem = ""
            for i in range(len(obj)):
                x = obj[i]
                if not self.exclude(i, x):
                    y = pathname + [ lastitem + ("[%d]" % i) ]
                    lst.append((i, x, y))
            for i, v, pn in lst:
                if self.showThis(i, v):
                    self.handleLeaf(v, depth+1, pn)
            for i, v, pn in lst:
                self.descend(v, depth+1, pn)
        elif type(obj) in (types.DictType,):
            keys = obj.keys()
            lst = [ ]
            if len(pathname) > 0:
                lastitem = pathname[-1]
                pathname = pathname[:-1]
            else:
                lastitem = ""
            for k in keys:
                x = obj[k]
                if not self.exclude(k, x):
                    y = pathname + [ lastitem + ("[%s]" % repr(k)) ]
                    lst.append((k, x, y))
            for k, v, pn in lst:
                if self.showThis(k, v):
                    self.handleLeaf(v, depth+1, pn)
            for k, v, pn in lst:
                self.descend(v, depth+1, pn)
        elif (hasattr(obj, "__class__") or
            type(obj) in (types.InstanceType, types.ClassType,
                          types.ModuleType, types.FunctionType)):
            ckeys = [ ]
            if True:
                # Look at instance variables, ignore class variables and methods
                if hasattr(obj, "__class__"):
                    ckeys = self.getAttributes(obj.__class__)
            else:
                # Look at all variables and methods
                ckeys = ( )
            keys = filter(lambda x: x not in ckeys, self.getAttributes(obj))
            lst = [ ]
            for k in keys:
                x = getattr(obj, k)
                if not self.exclude(k, x):
                    lst.append((k, x, pathname + [ k ]))
            for k, v, pn in lst:
                if self.showThis(k, v):
                    self.handleLeaf(v, depth+1, pn)
            for k, v, pn in lst:
                self.descend(v, depth+1, pn)

def standardExclude(attr, obj):
    # This is specific to the codebase I am currently working in.
    # These classes have a lot of internals that are rarely of interest.
    from MWsemantics import MWsemantics
    from GLPane import GLPane
    return isinstance(obj, MWsemantics) or isinstance(obj, GLPane)

def objectBrowse(obj, maxdepth=5, exclude=standardExclude, showThis=None, outf=sys.stderr):
    od = ObjectDescender(maxdepth=maxdepth, outf=outf)
    if showThis != None:
        od.showThis = showThis
    od.exclude = exclude
    od.descend(obj, pathname=['arg'])

def findChild(obj, showThis, maxdepth=8):
    # Drill down deeper because we're being more selective
    def prefix(depth, pn):
        # no indentation
        return (".".join(pn) + ": ")
    f = Finder(maxdepth=maxdepth)
    f.showThis = showThis
    f.prefix = prefix
    f.descend(obj, pathname=['arg'])
