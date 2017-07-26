""" 
    Module  : rubstr
    Author  : Snarkturne
    Version : 0.91 

    Evaluate expressions in strings 
    (the Ruby way : "Hello world number #{n+1}")

    from rubstr import rstr
    a,b=5,6
    print(rstr("If you add #{a} and #{b}, you'll get #{a+b}."))
    
    Note that the eval fonction is used. So, :
        rstr("Your files are #{os.listdir()}") 
    will give the list of your files if module os have been imported.
    (Using rstr can delete your files and do about everything that can be 
    done with Python, don't use rstr on unstrusted sources

    v 0.91 : 
       Added the access to callee locals
"""
import re
    
def _split(stri) :
    """ Split the initial string into normal strings and expressions 
    to evaluate (enclosed in #{...})
    """
    def analyse(s) :
        v=re.match("#{(.*)}$",s)
        if v : return ("E",v.group(1))
        return ("S",s)
    lst=re.split("(#{[^}]*})",stri)
    return [analyse(c) for c in lst]

def _eval(lstr,locals) :
    """ Evaluate parts of the string. Normal parts ("S") are not modified.
    Expression parts ("E") are evaluated (using eval).
    """
    l=[]
    for t,s in lstr :
        if t=="S" : l.append(s)
        if t=="E" : l.append(str(eval(s,None,locals)))
    return l
    
def rstr(stri) :
    """ Split the string, evaluates expressions, and reconstruct 
    the result.
    """
    import inspect
    f = inspect.currentframe()
    locals=f.f_back.f_locals
    return "".join(_eval(_split(stri),locals))


def testme() :
    n=4
    print(rstr("n=#{n}"))
    
if __name__=='__main__' :
    a,b=5,6
    print(rstr("If you add #{a} and #{b}, you'll get #{a+b}."))
    testme()
