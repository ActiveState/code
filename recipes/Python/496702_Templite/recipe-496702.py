import re


class Templite(object):
    delimiter = re.compile(r"\$\{(.*?)\}\$", re.DOTALL)
    
    def __init__(self, template):
        self.tokens = self.compile(template)
    
    @classmethod
    def from_file(cls, file):
        """
        loads a template from a file. `file` can be either a string, specifying
        a filename, or a file-like object, supporting read() directly
        """
        if isinstance(file, basestring):
            file = open(file)
        return cls(file.read())
    
    @classmethod
    def compile(cls, template):
        tokens = []
        for i, part in enumerate(cls.delimiter.split(template)):
            if i % 2 == 0:
                if part:
                    tokens.append((False, part.replace("$\\{", "${")))
            else:
                if not part.strip():
                    continue
                lines = part.replace("}\\$", "}$").splitlines()
                margin = min(len(l) - len(l.lstrip()) for l in lines if l.strip())
                realigned = "\n".join(l[margin:] for l in lines)
                code = compile(realigned, "<templite %r>" % (realigned[:20],), "exec")
                tokens.append((True, code))
        return tokens
    
    def render(__self, __namespace = None, **kw):
        """
        renders the template according to the given namespace. 
        __namespace - a dictionary serving as a namespace for evaluation
        **kw - keyword arguments which are added to the namespace
        """
        namespace = {}
        if __namespace: namespace.update(__namespace)
        if kw: namespace.update(kw)
        
        def emitter(*args):
            for a in args: output.append(str(a))
        def fmt_emitter(fmt, *args):
            output.append(fmt % args)
        namespace["emit"] = emitter
        namespace["emitf"] = fmt_emitter
        
        output = []
        for is_code, value in __self.tokens:
            if is_code:
                eval(value, namespace)
            else:
                output.append(value)
        return "".join(output)
    
    # shorthand
    __call__ = render

---------
example:
---------
>>> from templite import Templite
>>>
>>> demo = r"""
... <html>
...     <body>
...         ${
...         def say_hello(arg):
...             emit("hello ", arg, "<br>")
...         }$
...
...         <table>
...             ${
...                 for i in range(10):
...                     emit("<tr><td> ")
...                     say_hello(i)
...                     emit(" </tr></td>\n")
...             }$
...         </table>
...
...         ${emit("hi")}$
...
...         tralala ${if x > 7:
...             say_hello("big x")}$ lala
...
...         $\{this is escaped starting delimiter
...
...         ${emit("this }\$ is an escaped ending delimiter")}$
...
...         ${# this is a python comment }$
...
...     </body>
... </html>
... """
>>>
>>> t = Templite(demo)
>>> print t(x = 8)

<html>
    <body>


        <table>
            <tr><td> hello 0<br> </tr></td>
<tr><td> hello 1<br> </tr></td>
<tr><td> hello 2<br> </tr></td>
<tr><td> hello 3<br> </tr></td>
<tr><td> hello 4<br> </tr></td>
<tr><td> hello 5<br> </tr></td>
<tr><td> hello 6<br> </tr></td>
<tr><td> hello 7<br> </tr></td>
<tr><td> hello 8<br> </tr></td>
<tr><td> hello 9<br> </tr></td>

        </table>

        hi

        tralala hello big x<br> lala

        ${this is escaped starting delimiter

        this }$ is an escaped ending delimiter



    </body>
</html>

>>>
