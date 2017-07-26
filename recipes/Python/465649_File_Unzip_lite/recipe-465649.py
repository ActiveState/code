import os, zipfile
from cStringIO import StringIO

def extract( filename, dir ):
    zf = zipfile.ZipFile( filename )
    namelist = zf.namelist()
    dirlist = filter( lambda x: x.endswith( '/' ), namelist )
    filelist = filter( lambda x: not x.endswith( '/' ), namelist )
    # make base
    pushd = os.getcwd()
    if not os.path.isdir( dir ):
        os.mkdir( dir )
    os.chdir( dir )
    # create directory structure
    dirlist.sort()
    for dirs in dirlist:
        dirs = dirs.split( '/' )
        prefix = ''
        for dir in dirs:
            dirname = os.path.join( prefix, dir )
            if dir and not os.path.isdir( dirname ):
                os.mkdir( dirname )
            prefix = dirname
    # extract files
    for fn in filelist:
        try:
            out = open( fn, 'wb' )
            buffer = StringIO( zf.read( fn ))
            buflen = 2 ** 20
            datum = buffer.read( buflen )
            while datum:
                out.write( datum )
                datum = buffer.read( buflen )
            out.close()
        finally:
            print fn
    os.chdir( pushd )
