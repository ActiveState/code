'''
A simple, embeddable templating language.  

Templates are executable Python code with strings embedded in them.  Template 
strings embedded in the code are emitted when the template is executed.
Variable substitution is performed using the common $var/${expr} notation.  The
${expr} form may include any expression, while the $var form may only contain 
a simple name.

A template string is a string used by itself on a line, not as part of an 
expression.  E.g.,

import sys
for count,segment in enumerate(sys.path):
  """
  $count: $segment
  """

Docstrings for modules or functions do not count as template strings and 
are not emitted.

Copyright (C) 2005 Kevin Schluff
License: Python license
'''

import string, re
import compiler
from compiler import ast, misc, visitor, pycodegen

class Template:
  """
  A Template is created from a Python source file with embedded 
  template strings.  Once created, a Template can  be reused by 
  calling emit() with different substitution variables.
  """

  def __init__(self, source):
    """
    Create a new template and compile it to bytecode.
    
    source - an open file or a string containing the template text.
    """
    if hasattr(source,'read'):
      filename = source.name
      source = source.read()
    else:
      filename = "<string>"
    self.code = TemplateCompiler().compile(source, filename)
      
  def emit(self, fd, **context):
    """
    Emit the text of the template, substituting the variables provided. 
    
    fd - A file-like object to write the output to.  E.g.,sys.stdout or StringIO.
    kwargs - Variables to substitute are passed as keyword arguments.
    """
    context['__StringTemplate'] = StringTemplate
    context['__template_fd'] = fd
    context['__EvalMapper'] = EvalMapper
    exec self.code in context
    
class TemplateCompiler(visitor.ASTVisitor):
  """
  The TemplateCompiler is an ASTVisitor that walks over the parsed AST, 
  transforming template strings into string.Templates.
  """
  # Strip a single leading newline and any tabs or spaces after the 
  # last newline.
  TEXT_RE = re.compile(r"\n?(.*\n)[ \t]*", re.DOTALL )
  
  def __init__(self):
    """
    Create a TemplateCompiler instance.
    """
    visitor.ASTVisitor.__init__(self)
    
  def compile(self, source, filename="<string>"):
    """
    Compile the template source into a code object suitable for execution
    with exec or eval.
    
    source - template (Python) source to compile.
    filename - the filename used in the compiled code.  This name will be
               used in tracebacks.
    """
    mod = compiler.parse(source)
    misc.set_filename(filename, mod)
    self.preorder(mod, self)
    generator = pycodegen.ModuleCodeGenerator(mod)
    code = generator.getCode()
    return code
    
  def visitStmt(self, node):
    """
    Visit a Stmt node to replace all of the template strings with 
    code that emits the string.
    """
    nodes = []
    for child in node.nodes:
      if isinstance(child, ast.Discard):
        children = self.replaceDiscard(child)
        for newNode in children:
          nodes.append(newNode)
      else:
        nodes.append(child)
            
    node.nodes = nodes
    
    for n in node.nodes:
      self.dispatch(n)
      
  def replaceDiscard(self, node):
    """
    Replace a single discard statement with a series of statements
    that write out the string. 
    """
    # Only operate on constant expressions
    if not isinstance(node.expr, ast.Const):
      return [node]

    value = self.TEXT_RE.sub(r"\1",node.expr.value)
    
    # This code replaces each template string
    subst = """
__mapper = __EvalMapper(globals(), locals())
__template_fd.write(__StringTemplate(%s).safe_substitute(__mapper))
""" % value.__repr__()

    module = compiler.parse(subst)
    nodes = module.node.nodes
        
    return nodes

class StringTemplate(string.Template):
  
    pattern = re.compile(r"""
    %(delim)s(?:
      (?P<escaped>%(delim)s) |   # Escape sequence of two delimiters
      (?P<named>%(id)s)      |   # delimiter and a Python identifier
      {(?P<braced>%(expr)s)} |   # delimiter and a braced identifier
      (?P<invalid>)              # Other ill-formed delimiter exprs
    )
   """ % {"delim":r"\$", "id":r"[_a-z][_a-z0-9]*", "expr":r".*?"},
     re.VERBOSE | re.IGNORECASE )
    
class EvalMapper:

    def __init__(self, globals_, locals_):
        self.globals = globals_
        self.locals = locals_

    def __getitem__(self, name):
        return eval(name, self.globals, self.locals)
              
if __name__ == "__main__":
  import sys
  template = Template(open(sys.argv[1]))
  template.emit(sys.stdout)
