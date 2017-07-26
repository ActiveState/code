import zipfile
import os
import cStringIO

def zipwalk(zfilename):
    """Zip file tree generator.

    For each file entry in a zip archive, this yields
    a two tuple of the zip information and the data
    of the file as a StringIO object.

    zipinfo, filedata

    zipinfo is an instance of zipfile.ZipInfo class
    which gives information of the file contained
    in the zip archive. filedata is a StringIO instance
    representing the actual file data.

    If the file again a zip file, the generator extracts
    the contents of the zip file and walks them.

    Inspired by os.walk .
    """

    tempdir=os.environ.get('TEMP',os.environ.get('TMP',os.environ.get('TMPDIR','/tmp')))
    
    try:
        z=zipfile.ZipFile(zfilename,'r')
        for info in z.infolist():
            fname = info.filename
            data = z.read(fname)
            extn = (os.path.splitext(fname)[1]).lower()

            if extn=='.zip':
                checkz=False
                
                tmpfpath = os.path.join(tempdir,os.path.basename(fname))
                try:
                    open(tmpfpath,'w+b').write(data)
                except (IOError, OSError),e:
                    print e

                if zipfile.is_zipfile(tmpfpath):
                    checkz=True

                if checkz:
                    try:
                        for x in zipwalk(tmpfpath):
                            yield x
                    except Exception, e:
                        raise
                    
                try:
                    os.remove(tmpfpath)
                except:
                    pass
            else:
                yield (info, cStringIO.StringIO(data))
    except RuntimeError, e:
        print 'Runtime Error'
    except zipfile.error, e:
        raise
                        
if __name__=="__main__":
    import sys
    
    for i,d in zipwalk(sys.argv[1]):
        print i.filename
    
    
