"""
DICTIONNARY INTERFACE FOR EDITING VALUES
creates labels/edits/menubutton widgets in a TkFrame to edit dictionary values
use: apply(frame,dict,position)
"""

import Tkinter as tk

def cbMenu(controlV,value,btn= None):
    controlV.set(str(value))
    if not (btn== None):
        btn.config(text= str(value))

def updateMB(ctrlV, value):
    ctrlV.set(value)
        
def doLambda(f,*args):
    """Tips: Create lambda within for loop with fixed local variable
    without interference across iterations"""
    def g(): return f(*args)
    return g


def apply(root,d,pos):
    """Creates interface for dictionnary d in root at given grid position """
    "TODO: repercuter kwargs"
    (x,y,w,h)= pos
    lbs= []    
    saisies= dict()    
    entries= dict()
    for (n,(k,v)) in enumerate(d.iteritems()):  
        assert (k not in saisies)        
        l= tk.Label(root,text=str(k))
        l.grid(row=n+x,column=y)               
        if isinstance(v,list):
            """value= list => multiple choice => use menubutton"""            
            #saisies[k]= tk.StringVar(name=str(n),value= str(v[0]))
            saisies[k]= tk.StringVar(value= str(v[0]))            
            ent=tk.Menubutton(root,textvariable=saisies[k],relief="sunken")
            ent.m=tk.Menu(ent,tearoff=0)
            ent.config(menu=ent.m)    
            for (kk,possible) in enumerate(v):             
                possibleSaved= "%s" %possible                 
                ent.m.add_command(label=str(possible), command= doLambda(updateMB,saisies[k],str(d[k][kk]) ) )
                print possible
        else:         
            """value is not a list => classical edit => use Entry""" 
            #saisies[k]= tk.StringVar(name=str(n),value= str(v))
            saisies[k]= tk.StringVar(value= str(v))   
            ent= tk.Entry(textvariable=saisies[k])#,width=30)
        ent.grid(row=n+x,column=y+1)     
        entries[k]= ent
    return saisies

def get(strVarDict):
    d= {}
    for (k,v) in strVarDict.iteritems():
        #try: v= float(v)
        #except: pass
        d[k]=v.get()
    return d
    

        
def main():
    "EXAMPLE"
    root = tk.Tk()
    #d= {'oui':1, 'non':'non'}
    d= {'oui':1,'a':'b', 'non':['?','!non'],'mode':[1.1,2.1,3.1]}
    
    v= tk.StringVar(value= "Open File Dialog")
    
    m=tk.Menubutton(root,textvariable=v,relief="raised")
    m.grid(row=2,column=1)
    mm=tk.Menu(m,tearoff=0)
    tk.Button(root, textvariable=v, command=lambda:v.set('oui')).grid(row=1,column=1)
    mm.add_command(label="go", command=lambda: cbMenu(v,"non"))
    m.config(menu=mm) 
    
    s= apply(root,d,(0,2,0,0))
    print isinstance(d, dict)
    root.mainloop()
    #print d
    print s
    for (k,v) in s.iteritems():
        print str(k), '->',str(v.get())
        
def testindependance():
    root = tk.Tk()
    d= {'oui':1,'a':'b', 'non':['?','!non'],'mode':[1.1,2.1,3.1]}
    s= apply(root,d,(0,2,0,0))
    
    dd= {'oui':1,'a':'b', 'non':['?','!non'],'mode':[1.1,2.1,3.1]}
    ss= apply(root,dd,(0,5,0,0))
    
    print "s =",s
    print "ss=",ss
    
    print isinstance(d, dict)
    root.mainloop()
    #print d
    #print s
    for (k,v) in s.iteritems():
        print str(k), '->',str(v.get())
    print "-"*10
    for (k,v) in ss.iteritems():
        print str(k), '->',str(v.get()) 
    print "="*10
    print get(s)
    print get(ss)
           

if __name__ == '__main__':
    main()
    #testindependance()

        
