"XYAPTU: Lightweight XML/HTML Document Template Engine for Python"

__version__ = '1.0.0'
__author__= [
  'Alex Martelli (aleax@aleax.it)', 
  'Mario Ruggier (mario@ruggier.org)'
]
__copyright__ = '(c) Python Style Copyright. All Rights Reserved. No Warranty.'
__dependencies__ = ['YAPTU 1.2, http://aspn.activestate.com/ASPN/Python/Cookbook/Recipe/52305']
__history__= {
  '1.0.0' : '2002/11/13: First Released Version',
}

####################################################
    
import sys, re, string
from yaptu import copier
        
class xcopier(copier):
  ' xcopier class, inherits from yaptu.copier '
  
  def __init__(self, dns, rExpr=None, rOpen=None, rClose=None, rClause=None, 
               ouf=sys.stdout, dbg=0, dbgOuf=sys.stdout):
    ' set default regular expressions required by yaptu.copier '

    # Default regexps for yaptu delimeters (what xyaptu tags are first converted to)
    # These must be in sync with what is output in self._x2y_translate
    _reExpression = re.compile('_:@([^:@]+)@:_')
    _reOpen       = re.compile('\++yaptu ')
    _reClose      = re.compile('--yaptu')
    _reClause     = re.compile('==yaptu ')
    
    rExpr         = rExpr  or _reExpression
    rOpen         = rOpen  or _reOpen
    rClose        = rClose or _reClose
    rClause       = rClause or _reClause

    # Debugging
    self.dbg = dbg
    self.dbgOuf = dbgOuf
    _preproc = self._preProcess
    if dbg: _preproc = self._preProcessDbg
    
    # Call super init
    copier.__init__(self, rExpr, dns, rOpen, rClose, rClause, 
                    preproc=_preproc, handle=self._handleBadExps, ouf=ouf)


  def xcopy(self, input=None):
    '''
    Converts the value of the input stream (or contents of input filename) 
    from xyaptu format to yaptu format, and invokes yaptu.copy
    '''
    
    # Read the input
    inf = input
    try: 
      inputText = inf.read()
    except AttributeError: 
      inf = open(input)
      if inf is None: 
        raise ValueError, "Can't open file (%s)" % input 
      inputText = inf.read()
    try:
      inf.close()
    except: 
      pass

    # Translate (xyaptu) input to (yaptu) input, and call yaptu.copy()
    from cStringIO import StringIO
    yinf = StringIO(self._x2y_translate(inputText))
    self.copy(inf=yinf)
    yinf.close()

  def _x2y_translate(self, xStr):
    ' Converts xyaptu markup in input string to yaptu delimeters '
        
    # Define regexps to match xml elements on.
    # The variations (all except for py-expr, py-close) we look for are: 
    # <py-elem code="{python code}" /> | 
    # <py-elem code="{python code}">ignored text</py-elem> | 
    # <py-elem>{python code}</py-elem>
    
    # ${py-expr} | $py-expr | <py-expr code="pvkey" />
    reExpr = re.compile(r'''
      \$\{([^}]+)\} |  # ${py-expr}
      \$([_\w]+) | # $py-expr
      <py-expr\s+code\s*=\s*"([^"]*)"\s*/> |
      <py-expr\s+code\s*=\s*"([^"]*)"\s*>[^<]*</py-expr> |
      <py-expr\s*>([^<]*)</py-expr\s*>
    ''', re.VERBOSE)
    
    # <py-line code="pvkeys=pageVars.keys()"/>
    reLine = re.compile(r'''
      <py-line\s+code\s*=\s*"([^"]*)"\s*/> |
      <py-line\s+code\s*=\s*"([^"]*)"\s*>[^<]*</py-line> |
      <py-line\s*>([^<]*)</py-line\s*>
    ''', re.VERBOSE)
    
    # <py-open code="for k in pageVars.keys():" />
    reOpen = re.compile(r'''
      <py-open\s+code\s*=\s*"([^"]*)"\s*/> |
      <py-open\s+code\s*=\s*"([^"]*)"\s*>[^<]*</py-open\s*> |
      <py-open\s*>([^<]*)</py-open\s*>
    ''', re.VERBOSE)
    
    # <py-clause code="else:" />
    reClause = re.compile(r'''
      <py-clause\s+code\s*=\s*"([^"]*)"\s*/> |
      <py-clause\s+code\s*=\s*"([^"]*)"\s*>[^<]*</py-clause\s*> |
      <py-clause\s*>([^<]*)</py-clause\s*>
    ''', re.VERBOSE)
    
    # <py-close />
    reClose = re.compile(r'''
      <py-close\s*/> |
      <py-close\s*>.*</py-close\s*>
    ''', re.VERBOSE)

    # Call-back functions for re substitutions 
    # These must be in sync with what is expected in self.__init__
    def rexpr(match,self=self): 
      return '_:@%s@:_' % match.group(match.lastindex)
    def rline(match,self=self): 
      return '\n++yaptu %s #\n--yaptu \n' % match.group(match.lastindex)
    def ropen(match,self=self): 
      return '\n++yaptu %s \n' % match.group(match.lastindex)
    def rclause(match,self=self): 
      return '\n==yaptu %s \n' % match.group(match.lastindex)
    def rclose(match,self=self): 
      return '\n--yaptu \n'

    # Substitutions    
    xStr = reExpr.sub(rexpr, xStr)
    xStr = reLine.sub(rline, xStr)
    xStr = reOpen.sub(ropen, xStr)
    xStr = reClause.sub(rclause, xStr)
    xStr = reClose.sub(rclose, xStr)

    # When in debug mode, keep a copy of intermediate template format
    if self.dbg:
      _sep = '====================\n'
      self.dbgOuf.write('%sIntermediate YAPTU format:\n%s\n%s' % (_sep, xStr, _sep))

    return xStr

  # Handle expressions that do not evaluate
  def _handleBadExps(self, s):
    ' Handle expressions that do not evaluate '
    if self.dbg: 
      self.dbgOuf.write('!!! ERROR: failed to evaluate expression: %s \n' % s)
    return '***! %s !***' % s

  # Preprocess code
  def _preProcess(self, s, why):
    ' Preprocess embedded python statements and expressions '
    return self._xmlDecode(s)
  def _preProcessDbg(self, s, why):
    ' Preprocess embedded python statements and expressions '
    self.dbgOuf.write('!!! DBG: %s %s \n' % (s, why))
    return self._xmlDecode(s)
  
  # Decode utility for XML/HTML special characters
  _xmlCodes = [
    ['"', '&quot;'],
    ['>', '&gt;'],
    ['<', '&lt;'],
    ['&', '&amp;'],
  ]
  def _xmlDecode(self, s):
    ' Returns the ASCII decoded version of the given HTML string. '
    codes = self._xmlCodes
    for code in codes:
      s = string.replace(s, code[1], code[0])
    return s


####################################################

if __name__=='__main__':

  ##################################################
  # Document Name Space (a dictionary, normally prepared by runtime application,
  # and that serves as the substitution namespace for instantiating a doc template).
  #
  DNS = {
    'pageTitle' : 'Event Log (xyaptu test page)',
    'baseUrl' : 'http://xproject.sourceforge.net/',
    'sid' : 'a1b2c3xyz',
    'session' : 1,
    'userName' : 'mario',
    'startTime' : '12:31:42',
    'AllComputerCaptions' : 'No',
    'ComputerCaption' : 'mymachine01',
    'LogSeverity' : ['Info', 'Warning', 'Error' ],
    'LogFileType' : 'Application',
    'logTimeStamp' : 'Event Log Dump written on 25 May 2001 at 13:55',
    'logHeadings' : ['Type', 'Date', 'Time', 'Source', 'Category', 'Computer', 'Message'] , 
    'logEntries' : [
      ['Info', '14/05/2001', '15:26', 'MsiInstaller', '0', 'PC01', 'winzip80 install ok...'],
      ['Warning', '16/05/2001', '02:43', 'EventSystem', '4', 'PC02', 'COM+ failed...'],      
      ['Error', '22/05/2001', '11:35', 'rasctrs', '0', 'PC03', '...', ' ** EXTRA ** ' ],
    ]
  }
  
  # and a function...
  def my_current_time():
    import time
    return str(time.clock())
  DNS['my_current_time'] = my_current_time

  '''  
  # To use functions defined in an external library
  import externalFunctionsLib
  dict['fcn'] = externalFunctionsLib 
  # which will therefore permit to call functions with: 
  ${fcn.somefun()}
  '''
  
  ##################################################
  # Sample page template that uses the xyaptu tags and pcdata expressions. 
  # Note that:
  #  - source code indentation here is irrelevant for xyaptu
  #  - xyaptu tags may span more than one source line
  #
  templateString = '''<html>
 <head>
  <title>$pageTitle</title>
 </head>
 <body bgcolor="#FFFFFF" text="#000000">
  
  <py-open code="if session:"/> 
   Logged on as $userName, since <py-expr>startTime</py-expr>
   (<a href="$baseUrl?sid=$sid&amp;linkto=Logout">Logout?</a>)
  <py-close/>
  <hr>
  <h1>${pageTitle}</h1>
  <hr>
  <p>${a bad expression}</p>
  <p>
   <b>Filtering Event Log With:</b><br>
   All Computers: $AllComputerCaptions <br>
   Computer Name: $ComputerCaption <br>
   Log Severity: 
    <py-open code="for LG in LogSeverity:"/> 
      $LG
    <py-close/> 
    <br>
   Log File Type: <py-expr code="LogFileType" />
  </p>
  <hr>
  <p>$logTimeStamp</p>
  
  <table width="100%" border="0" cellspacing="0" cellpadding="2">

   <tr valign="top" align="left">
    <py-open code = "for h in logHeadings:" > code attribute takes precedence 
     over this text, which is duly ignored </py-open>
     <th>$h</th>
    <py-close/>
   </tr>

   <py-line
               code = "numH=len(logHeadings)" 
                                                />
   
   <py-open code="for logentry in logEntries:"/>
    <tr valign="top" align="left">
     <py-open>for i in range(0,len(logentry)):</py-open>
      <py-open code="if i &lt; numH:" />
       <td>${logentry[i]}</td>
      <py-clause code="else:" />
       <td bgcolor="#cc0000">Oops! <!-- There's more log entry fields than headings! --></td>
      <py-close/>
     <py-close>### close (this is ignored) </py-close>
    </tr>
   <py-close/>
   
  </table>
  <hr>
  Current time: ${my_current_time()}
  <hr>
 </body>
</html>
  '''

  ##################################################
  # Set a filelike object to templateString 
  from cStringIO import StringIO
  templateStream = StringIO(templateString)
  
  ##################################################
  # Initialise an xyaptu xcopier, and call xcopy
  xcp = xcopier(DNS)
  xcp.xcopy(templateStream)


  ##################################################
  # Test DBG 1
  # Set dbg ON (writing dbg statements on output stream)
  '''
  xcp = xcopier(DNS, dbg=1)
  xcp.xcopy(templateStream)
  '''
  
  ##################################################
  # Test DBG 2
  # Write dbg statements to a separate dbg stream
  '''
  dbgStream = StringIO()
  dbgStream.write('DBG info: \n')
  xcp = xcopier(DNS, dbg=1, dbgOuf=dbgStream)
  xcp.xcopy(templateStream)
  print dbgStream.getvalue()
  dbgStream.close()
  '''
  
####################################################  
