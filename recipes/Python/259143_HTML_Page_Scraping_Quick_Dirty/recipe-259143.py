from re import compile, sub, DOTALL, IGNORECASE

RE = """\
(?:Schedule:&nbsp;</B></TD><TD><font face="Arial, Helvetica, sans-serif" size="2">(?P<schedule>[\d]+))\
|\
(?:http://data6.archives.ca/exec/getSID.pl\?f=(?P<URL>.{15}))\
"""

compiledRE = compile ( RE, DOTALL or IGNORECASE )

def handleMatch ( match ) :
    global schedule
    if match . groups ( ) [ 0 ] :
        schedule = match . groups ( ) [ 0 ]
    else :
        if match . groups ( ) [ 1 ] and schedule == '1' :
            print match . groups ( ) [ 1 ]
    return ''

htm = file ( 'cornwall.htm' ) . read ( )

sub ( compiledRE, handleMatch, htm )
