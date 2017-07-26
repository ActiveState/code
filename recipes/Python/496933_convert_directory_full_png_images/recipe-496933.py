import sys
import os
import binascii
from glob import glob

s_header="""import wx
from cStringIO import StringIO
from binascii import a2b_base64

class Images:
    def __init__(self):
        for name in _names:
            img = wx.ImageFromStream(StringIO(a2b_base64(eval(\"_\"+name))))
            img.ConvertAlphaToMask(100)
            exec(\"self.bmp_\"+name+\"=img.ConvertToBitmap()\")
        self._names=_names\n
"""

max_line=78

def split_string(s):
    ls=len(s)
    so=""
    while len(s)>max_line-1:
        so+=s[:max_line-1]+"\\\n"
        s=s[max_line-1:]

    so+=s
    return so

def split_list(s):
    b=s
    s_out=""
    while(len(b)>max_line):
        c=b[0:max_line]
        tail,head=c[::-1].split(",",1)
        head,tail=head[::-1],tail[::-1]
        s_out+=head+",\n"
        b="    "+tail+b[max_line:]

    s_out+=b
    return s_out

def convert_base64(s,var_name):
    so=binascii.b2a_base64(s)
    print "converting %s: %d->%d" % (var_name,len(s),len(so))

    r_out="%s=\"" % var_name
    r_out+=so[:-1]+"\""

    return r_out

def convert(s,var_name):
    l=len(s)
    print "converting %s (%d chars)" % (var_name,l)

    r_out="%s=\"" % var_name
    for c in s:
        o=ord(c)
        if c=="\"":
            c_out="\\\""
        elif c=="\'":
            c_out="\\\'"
        elif c=="\\":
            c_out="\\\\"
        elif o>31 and o<127:
            c_out=c
        elif o<16:
            c_out="\\x0"+hex(o)[2:]
        else:
            c_out="\\x"+hex(o)[2:]

        r_out+=c_out

    r_out+="\""
    return r_out

def main(argv=None):
    #for the time being, get the list from glob...
    png_files=glob(os.path.join(".",'*.png'))

    v_list=[]
    s_vars=""
    for fn in png_files:
        s=open(fn,"rb").read()
        p,fn=os.path.split(fn)
        v=fn[:-4]
        v=v.replace("stock_","")
        v=v.replace("3d-","")
        v=v.replace("-16","")
        v=v.replace("-","_")
        v=v.replace(" ","_")
        v=v.replace(".","_")

        v_list.append(v)

        r=split_string(convert_base64(s,"_"+v))
        s_vars+=r+"\n\n"

    s_names=split_list("_names="+str(v_list))+"\n\n"

    if os.path.exists("images.py"):
        try:
            os.rename("images.py","images.bak")
            print "Your old images.py was renamed images.bak"
        except:
            print "Sorry, I don\'t do deletes..."
            print "Please delete images.bak yourself"

    f=open("images.py","w")
    f.write(s_header)
    f.write(s_names)
    f.write(s_vars)
    f.close()

if __name__ == '__main__':
    main()
