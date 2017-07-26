# -- coding: iso8859-1
"""Generic option parser class. This class can be used
to write code that will parse command line options for
an application by invoking one of the standard Python
library command argument parser modules optparse or
getopt.

The class first tries to use optparse. It it is not there
(< Python 2.3), it invokes getopt. However, this is
transparent to the application which uses the class.

The class requires a dictionary with entries of the following
form for each command line option.

'option_var' :   ('short=<short option>','long=<long option>',
                  'help=<help string>', 'meta=<meta variable>',
                  'default=<default value>', 'type=<option type>')

where, 'option_var' is the key for the option in the final
dictionary of option-value pairs. The value is a tuple of
strings, where each string consists of entries of the form,

'key=value', where 'key' is borrowed from the way optparse
represents each variables for an option setting.

To parse the arguments, call the method 'parse_arguments'.
The return value is a dictionary of the option-value pairs."""

import sys

__author__="Anand Pillai"

class GenericOptionParserError(Exception):
    
    def __init__(self,value):
        self.value = value

    def __str__(self):
        return str(self.value)
    
class GenericOptionParser:
    """ Generic option parser using
    either optparse or getopt """

    def __init__(self, optmap):
        self._optmap = self._parse_optmap(optmap)
        self._optdict = {}
        self.maxw = 24
        
    def _parse_optmap(self, map):
        """ Internal method -> Parse option
        map containing tuples and convert the
        tuples to a dictionary """

        optmap = {}
        for key,value in map.items():
            d = {}
            for item in value:
                if not item: continue
                var,val=item.split('=')
                d[var]=val
                
            optmap[key] = d

        return optmap
        
    def parse_arguments(self):
        """ Parse command line arguments and
        return a dictionary of option-value pairs """

        try:
            self.optparse = __import__('optparse')
            # For invoking help, when no arguments
            # are passed.
            if len(sys.argv)==1:
                sys.argv.append('-h')

            self._parse_arguments1()
        except ImportError:
            try:
                import getopt
                self.getopt = __import__('getopt')                
                self._parse_arguments2()
            except ImportError:
                raise GenericOptionParserError,'Fatal Error: No optparse or getopt modules found'

        return self._optdict
                
    def _parse_arguments1(self):
        """ Parse command-line arguments using optparse """

        p = self.optparse.OptionParser()
        
        for key,value in self._optmap.items():
            # Option destination is the key itself
            option = key
            # Default action is 'store'
            action = 'store'
            # Short option string
            sopt = value.get('short','')
            # Long option string
            lopt = value.get('long','')
            # Help string
            helpstr = value.get('help','')
            # Meta var
            meta = value.get('meta','')
            # Default value
            defl = value.get('default','')
            # Default type is 'string'
            typ = value.get('type','string')
            
            # If bool type...
            if typ == 'bool':
                action = 'store_true'
                defl = bool(str(defl) == 'True')

            if sopt: sopt = '-' + sopt
            if lopt: lopt = '--' + lopt
            
            # Add option
            p.add_option(sopt,lopt,dest=option,help=helpstr,metavar=meta,action=action,
                         default=defl)

        (options,args) = p.parse_args()
        self._optdict = options.__dict__

    def _parse_arguments2(self):
        """ Parse command-line arguments using getopt """

        # getopt requires help string to
        # be generated.
        if len(sys.argv)==1:
            sys.exit(self._usage())
        
        shortopt,longopt='h',['help']
        # Create short option string and long option
        # list for getopt
        for key, value in self._optmap.items():
            sopt = value.get('short','')
            lopt = value.get('long','')
            typ = value.get('type','string')            
            defl = value.get('default','')

            # If bool type...
            if typ == 'bool':
                defl = bool(str(defl) == 'True')
            # Set default value
            self._optdict[key] = defl

            if typ=='bool':
                if sopt: shortopt += sopt
                if lopt: longopt.append(lopt)
            else:
                if sopt: shortopt = "".join((shortopt,sopt,':'))
                if lopt: longopt.append(lopt+'=')

        # Parse
        (optlist,args) = self.getopt.getopt(sys.argv[1:],shortopt,longopt)

        # Match options
        for opt,val in optlist:
            # Invoke help
            if opt in ('-h','--help'):
                sys.exit(self._usage())
                
            for key,value in self._optmap.items():
                sopt = '-' + value.get('short','')
                lopt = '--' + value.get('long','')
                typ = value.get('type','string')
                
                if opt in (sopt,lopt):
                    if typ=='bool': val = True
                    self._optdict[key]=val
                    del self._optmap[key]
                    break

    def _usage(self):
        """ Generate and return a help string
        for the program, similar to the one
        generated by optparse """

        usage = ["usage: %s [options]\n\n" % sys.argv[0]]
        usage.append("options:\n")

        options = [('  -h, --help', 'show this help message and exit\n')]
        maxlen = 0
        for value in self._optmap.values():
            sopt = value.get('short','')
            lopt = value.get('long','')
            help = value.get('help','')
            meta = value.get('meta','')
            
            optstr = ""
            if sopt: optstr="".join(('  -',sopt,meta))
            if lopt: optstr="".join((optstr,', --',lopt))
            if meta: optstr="".join((optstr,'=',meta))
            
            l = len(optstr)
            if l>maxlen: maxlen=l
            options.append((optstr,help))
            
        for x in range(len(options)):
            optstr = options[x][0]
            helpstr = options[x][1]
            if maxlen<self.maxw - 1:
                usage.append("".join((optstr,(maxlen-len(optstr) + 2)*' ', helpstr,'\n')))
            elif len(optstr)<self.maxw - 1:
                usage.append("".join((optstr,(self.maxw-len(optstr))*' ', helpstr,'\n')))
            else:
                usage.append("".join((optstr,'\n',self.maxw*' ', helpstr,'\n')))                

        return "".join(usage)

if __name__=="__main__":
    d={ 'infile' : ('short=i','long=in','help=Input file for the program',
                    'meta=IN'),
        'outfile': ('short=o','long=out','help=Output file for the program',
                    'meta=OUT'),
        'verbose': ('short=V','long=verbose','help=Be verbose in output',
                    'type=bool') }

    g=GenericOptionParser(d)
    optdict = g.parse_arguments()
 
    for key,value in optdict.items():
         # Use the option and the value in
         # your program
         ...
