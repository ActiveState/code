import re
import Tkinter, tkFileDialog
root = Tkinter.Tk()
root.withdraw()

p6 = re.compile("#[0-9a-f]{6};", re.IGNORECASE)
p3 = re.compile("#[0-9a-f]{3};", re.IGNORECASE)
filepath = tkFileDialog.askopenfilename(title= "file?",)
content = file(filepath,'r').read()

def Modify (content):
    text = content.group().lower()
    code = {}
    l1="#;0123456789abcdef"
    l2="#;fedcba9876543210"
    for i in range(len(l1)):
        code[l1[i]]=l2[i]
    inverted = ""
    for j in text:
        inverted += code[j]
    return inverted

content = p6.sub(Modify,content)
content = p3.sub(Modify,content)

filepath = filepath[:-4]+"MOD.css"
out = file(filepath,'w')
out.write(content)
out.close()
