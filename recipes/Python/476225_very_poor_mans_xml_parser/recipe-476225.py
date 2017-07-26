#  a quick and dirty xml module for parsing and generating xml/html
#
#  this is a very poor man's xml parser
#  it uses the python syntax parser for parsing xml code
#  and defines a tag class called T. xml code is first translated to
#  valid python code and then evaluated. works also under jython.
#
# (c) f.jamitzky 2006

class T:
    def __init__(self,name,args=[]):
        arglist=name.split(" ")
        self._name=arglist[0]
        self._kw={}
        self._args=args
        if len(arglist)>1:
            kw={}
            for i in arglist[1:]:
                key, val= i.split("=")
                kw[key]=val
            self._kw=kw
    def __len__(self):
        return len(self._args)
    def __str__(self):
        if self._args==[]:
            if self._kw=={}:
                txt="<"+self._name+"/>"
            else:
                txt="<"+self._name
                for i in self._kw.keys():
                    txt+=" "+str(i)+"="+str(self._kw[i])+" "
                txt=txt[:-1]+"/>"
        else:
            if self._kw=={}:
                txt="<"+self._name+">"
            else:
                txt="<"+self._name
                for i in self._kw.keys():
                    txt+=" "+str(i)+"="+str(self._kw[i])+" "
                txt=txt[:-1]+">"
            for arg in self._args:
                txt+=str(arg)
            txt+="</"+self._name+">"
        return txt
    def __repr__(self):
        return str(self)
    def __getitem__(self,key):
        if type(key)==type(0):
            return self._args[key]
        elif type(key)==type(""):
            return self._kw[key]
    def __setitem__(self,key,value):
        if type(key)==type(0):
            if key<len(self._args):
                self._args[key]=value
            else:
                self._args.insert(key,value)
        else:
            self._kw[key]=value
    def keys(self):
        return self._kw.keys()
    def tags(self):
        lst=[]
        for i in range(len(self)):
            try:
                lst.append(self[i]._name)
            except:
                pass
        return lst

    def get_tag_by_name(self,strg):
        lst=[]
        for i in range(len(self)):
            try:
                if self[i]._name==strg:
                    lst.append(self[i])
            except:
                pass
        if len(lst)==1:
            return lst[0]
        else:
            return lst
    def __getattr__(self,key):
        try:
            return self.get_tag_by_name(key)
        except:
            if self.__dict__.has_key(key):
                return self.__dict__[key]
            else:
                raise AttributeError, "Name does not exist '%s.'" % (key)
    def append(self,val):
        self._args.append(val)

def xml2code(instr):
    data=instr.replace("[","<lbracket/>").replace("]","<rbracket/>")
    data=data.replace("\n","").replace('"',"'")
    data=data.replace("?>","?/>").replace("-->","--/>")
    data=data.replace("</","[]endtag[").replace("/>","[]mptytag[")
    data=data.replace("<","[]starttag[").replace(">","[]closetag[")
    data=data.split("[")
    outstr=''
    i=-1
    lendata=len(data)
    while i<lendata-1:
        i+=1
        x=data[i]
        x=x.strip()
        if len(x)==0:
            continue
        if x[0]=="]":
            if x[1]=="s":
                outstr+='T("'+data[i+1]+'",['
                i=i+2
                if data[i][0:2]=="]m":
                    outstr+=']),'
            elif x[1]=="e":
                outstr+=']),'
                i=i+2
        else:
            outstr+='"'+x+'",'
    outstr="T('root',["+outstr+"])"
    outstr=outstr.replace(",)",")")
    return outstr

def xml(strg):
    return eval(xml2code(strg))[0]

print "parsing xml:"

data="""<a><a b='a'><b a='b'/></a><b>/a</b>b<a/><a/></a>"""
print "xml string:"
print data

tt=xml(data)

print "print:"
print tt
print "print tags:"
print tt.tags()
print "get tag 'a':"
print tt.a

print "generating html:"
html=xml("<html><head/><body/></html>")
html.body.append("Hello World from jython")
html.head['title']="Hello World"
print html
print ""
