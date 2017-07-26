#!/usr/bin/python
import fnmatch, ftplib, optparse, os, stat, string, sys, time

class FtpWalker:
    def __init__( self, site, user, passwd ):
        self.ftp = ftplib.FTP( site, user, passwd )
    def cd( self, path ):
        try:
            self.ftp.cwd( path )
        except:
            return False
        else:
            return True
    def pwd( self ):
        return self.ftp.pwd()
    def get( self, fileinfo, binary=True, callback=None ):
        status = alreadydownloaded( fileinfo )
        if status == DOWNLOAD_NONE: return
        if not callback:
            localfile = createfile( fileinfo, binary, status == DOWNLOAD_PARTIAL )
            callback  = localfile.write
        try:
            filename = fileinfo.longname
            getstr = "RETR %s" % fileinfo.name
            if binary:
                if status == DOWNLOAD_PARTIAL:
                    self.ftp.retrbinary( getstr, callback, rest=os.path.getsize( filename ) )
                else:
                    self.ftp.retrbinary( getstr, callback )
            else:
                self.ftp.retrlines( getstr, callback )
        finally: 
            if localfile:
                localfile.close()
                os.utime( filename, (fileinfo.date, fileinfo.date) )
                os.chmod( filename, fileinfo.mode )
    def ls( self, cwd ):
        lines = []
        self.ftp.retrlines( "LIST", lines.append )
        return map( lambda x: extract_info( cwd, x ), lines ) 

DOWNLOAD_FULL, DOWNLOAD_PARTIAL, DOWNLOAD_NONE = 0, 1, 2 

def alreadydownloaded( fileinfo ):
    f = fileinfo.longname
    if os.path.isfile( f ):
        ldate, rdate = os.path.getmtime( f ), fileinfo.date
        lsize, rsize = os.path.getsize( f ),  fileinfo.size
        if round( ldate ) == round( rdate ):
            if lsize == rsize:
                return DOWNLOAD_NONE    # already downloaded
            else:
                return DOWNLOAD_PARTIAL # partially downloaded
        else:
            newfilename = mknewversion( fileinfo.path, fileinfo.name )
            os.rename( fileinfo.longname, newfilename )
            return DOWNLOAD_FULL        # old version, rename
    else:
        return DOWNLOAD_FULL            # no file, download

def mknewversion( path, filename ):
    version = 1
    def mkversion( version ):
        return os.path.join( path, ".%s.%03d" % (filename, version) )
    longname = mkversion( version )
    while os.path.exists( longname ):
        version += 1
        longname = mkversion( version )
    return longname
 
def iff( test_, then_, else_ ): # then_, else_ always get evaled so pls be atoms
    if test_:
        return then_
    else:
        return else_

def createfile( fileinfo, binary, append ):
    fname = fileinfo.longname
    if not os.path.isdir( fileinfo.path ):
        os.makedirs( fileinfo.path )
    permissions = iff( binary, 'wb', 'w' )
    if append and os.path.isfile( fname ):
        permissions += 'a'
        perm = os.stat( fname )[stat.ST_MODE]
        if not perm & stat.S_IWUSR:
            os.chmod( fname, perm | stat.S_IWUSR )
    return file( fname, permissions )

curr_year_fmt, prev_year_fmt, unified_fmt = '%b %d %H:%M', '%b %d  %Y', '%Y-%m-%d-%H:%M'

def updatetuple( t, i, x ): # insert x into the ith field of tuple, t
    l = list( t )
    return tuple( l[:i] + [x] + l[i+1:] )

def parsePrevYear( date ): return time.strptime( date, prev_year_fmt )
def parseCurrYear( date ):
    datewith1900 = time.strptime( date, curr_year_fmt )
    currentYear  = time.gmtime()[0]
    return updatetuple( datewith1900, 0, currentYear )

def dateParser( date ): return iff( ':' in date, parseCurrYear, parsePrevYear )
def parseDate( date ):  return time.mktime( dateParser( date )( date ) )

def displayDate( date ):
    date_struct, curr_struct = time.gmtime( date ), time.gmtime()
    date_year, curr_year = date_struct[0], curr_struct[0]
    year_fmt = iff( date_year == curr_year, curr_year_fmt, prev_year_fmt )
    return time.strftime( year_fmt, date_struct )

R_MSK, W_MSK, X_MSK, Z_MSK =   4,   2,   1,   0
R_STR, W_STR, X_STR, Z_STR = 'r', 'w', 'x', '-'

def str2mode( str ):
    r, w, x = str[0] == R_STR,  str[1] == W_STR,  str[2] == X_STR
    return iff( r, R_MSK, Z_MSK ) | iff( w, W_MSK, Z_MSK ) | iff( x, X_MSK, Z_MSK )

def mode2str( mode ):
    r, w, x = mode & R_MSK, mode & W_MSK, mode & X_MSK
    return iff( r, R_STR, Z_STR ) + iff( w, W_STR, Z_STR ) + iff( x, X_STR, Z_STR )

def str2fullmode( str ):
    u, g, o = str[0:3], str[3:6], str[6:9]
    return str2mode( u ) << 6 | str2mode( g ) << 3 | str2mode( o )

def fullmode2str( mode ):
    u, g, o = mode >> 6 & 0x7, mode >> 3 & 0x7, mode & 0x7
    return mode2str( u ) + mode2str( g ) + mode2str( o )

def str2perm( str ):
    return str[0] == 'd', str[0] == 'l', str2fullmode( str[1:] )

def perm2str( isdir, islink, mode ):
    return iff( isdir, 'd', iff( islink, 'l', '-' ) ) + fullmode2str( mode )

def extract_info( cwd, line ):
    fullmode, links, owner, group, size, rest = line.split( None, 5 )
    isdir, islink, mode = str2perm( fullmode )
    dateStr, name = rest[:12], rest[13:]
    date = parseDate( dateStr )
    return FileInfo( cwd, name, fullmode, isdir, islink, mode, int( links ), owner, group, int( size ), dateStr, date)

class FileInfo:
    def __init__( self, path, name, modeStr, isdir, islink, mode, links, owner, group, size, dateStr, date, line ):
        self.path, self.name, self.isdir, self.islink = path, name, isdir, islink
        self.modeStr, self.mode, self.owner, self.group = modeStr, mode, owner, group
        self.links, self.size, self.dateStr, self.date = links, size, dateStr, date
        self.longname, self.age, self.line = os.path.join( path, name ), now - self.date, line

def dropslashes( str ): 
    i, n = 0, len( str )
    while i < n and str[i] == '/': i += 1
    return str[i:]

def excluded( exclude_patterns, dir ):
    for exclude_pattern in exclude_patterns:
        if pattern( exclude_pattern, dir ):
            return True
    return False

def listSiteGen( walker, dir, opts ):
    path = walker.pwd()
    if not excluded( opts.exclude, dir ) and walker.cd( dir ):
        for info in walker.ls( dropslashes( os.path.join( path, dir ) ) ):
            if info.isdir:
                for rec_info in listSiteGen( walker, info.name, opts ):
                    yield rec_info
            else:
                yield info
    walker.cd( path )

def ftpfind( walker, dir, opts ):
    for fileinfo in listSiteGen( walker, dir, opts ):
        if opts.expr( fileinfo ):
            print "%s" % opts.printer( fileinfo )
            if not opts.test:
                walker.get( fileinfo )

def date( d, f=None ):
    if f:
        return time.mktime( time.strptime( d, f ) )
    else:
        return parseDate( d )

def pattern( p, v ): return fnmatch.fnmatch( v, p )
kilobyte = 1024; megabyte = kilobyte * kilobyte; gigabyte = kilobyte * megabyte; terabyte = kilobyte * gigabyte
second = 1; minute = 60*second; hour = 60*minute; day = 24*hour; week = 7*day; year = 52*week
 
def expr_cb( option, opt_str, value, parser ): parser.values.expr = eval( "lambda file: " + value )
def print_cb( option, opt_str, value, parser ): parser.values.printer = eval( "lambda file: " + value )

now = time.mktime( time.gmtime() ) # used by age filter

def daystart_cb( option, opt_str, value, parser ):
    global now
    x = time.gmtime()
    start_of_day = x[0], x[1], x[2], 0, 0, 0, x[6], x[7], x[8]
    now = time.mktime( start_of_day )

def_printer=lambda file: file.line
def_expr=lambda file: True

def parse_command_line():
    parser = optparse.OptionParser()
    parser.set_defaults( user="anonymous", password="ftpfind@sf.net", expr=def_expr, test=False, exclude=[], printer=def_printer  )
    parser.add_option( "-e", "--expr",     action="callback", callback=expr_cb, type="string", help="use the python expression, lambda file: <EXPR>, as a filter (must return boolean)", metavar="EXPR" )
    parser.add_option( "-p", "--password", help="specify the password to use", metavar="PASSWD" )
    parser.add_option( "--print", action="callback", callback=print_cb, type="string", help="use the printer, lambda file: <EXPR>, to print file summary (must return string)", metavar="EXPR" )
    parser.add_option( "-s", "--daystart", action="callback", callback=daystart_cb, help="calculate ages from today @ 00:00" )
    parser.add_option( "-t", "--test",     action ="store_true", help="print filename but do not perform file transfer" )
    parser.add_option( "-u", "--user",     help="specify the username to use", metavar="USER" )
    parser.add_option( "-x", "--exclude",  action="append", help="do not traverse this directory", metavar="DIR" )
    return parser.parse_args()

if __name__ == '__main__':
    opts, args = parse_command_line()
    site, dirs = args[0], args[1:]
    if len( dirs ) == 0: dirs = ['/']
    try:
        walker = FtpWalker( site, opts.user, opts.password )
    except:
        print "Couldn't authenticate '%s' with password '%s' on %s" % (opts.user, opts.password, site)
        sys.exit(3)
    else:
        for dir in dirs:
            ftpfind( walker, dir, opts )
