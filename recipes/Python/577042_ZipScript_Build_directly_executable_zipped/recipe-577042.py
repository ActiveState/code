#####################################
def makeCheck( target, depend ):  # version 2010/02/11
    try:
        targmod = os.stat( target ).st_mtime
        if depend is not None:
            for ix in depend:
                if os.stat( ix ).st_mtime > targmod:
                    if debug:
                        print("makeCheck:",
                              target, targmod,
                              ix, os.stat( ix ).st_mtime
                              )
                        return True
        return False
    except:
        return True
#####################################
def zipScript( dest, main, progs = None, helps = None, compile = False
               ):  # version 2010/02/11
    """main gets renamed to __main__.py in the zip file
progs are a list of programs or modules to be included, source or compiled
helps is a list of helper modules to be included, source or compiled
"""
    tozip = []
    toremove = []
    funnymain = "__main__.py"
    
    if makeCheck( dest, (main,)) \
            or makeCheck( dest, progs ) \
            or makeCheck( dest, helps ):        
        # only if it is out of date

        import zipfile
        zf = zipfile.ZipFile( dest, "w", zipfile.ZIP_DEFLATED )

        if compile:
            import py_compile
            ixc = funnymain + "c"
            toremove.append( ixc )
            tozip.append( ixc )
            py_compile.compile( main, ixc, doraise = True )
            for ix in progs:
                ixc = ix + "c"
                toremove.append( ixc )
                tozip.append( ixc )
                py_compile.compile( ix, ixc, doraise = True )
            for ix in helps:
                ixc = ix + "c"
                toremove.append( ixc )
                tozip.append( ixc )
                py_compile.compile( ix, ixc, doraise = True )
        else:
            for ix in progs:
                tozip.append( ix )
            for ix in helps:
                tozip.append( ix )
            zf.write( ix, funnymain )

        for ix in tozip:
            zf.write( ix )
        zf.close()

        for ix in toremove:
            os.remove( ix )
#####################################
