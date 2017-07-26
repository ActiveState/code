import gc

def dump_garbage():
    """
    show us what's the garbage about
    """
        
    # force collection
    print "\nGARBAGE:"
    gc.collect()

    print "\nGARBAGE OBJECTS:"
    for x in gc.garbage:
        s = str(x)
        if len(s) > 80: s = s[:80]
        print type(x),"\n  ", s

if __name__=="__main__":
    import gc
    gc.enable()
    gc.set_debug(gc.DEBUG_LEAK)

    # make a leak
    l = []
    l.append(l)
    del l

    # show the dirt ;-)
    dump_garbage()
  
