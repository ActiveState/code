import re, sys

def main(from_tabs, to_tabs, fname):
    """
    Usage sample: 
     > reindent 3 4 mms.py
     processed mms.py, from 3 to 4 spaces. Output in mms.py.out.py.
     Lines 317, empty 51, not matching indent 50, matching indent 216 (68.14 %).
    """
    from_tabs, to_tabs = int(from_tabs), int(to_tabs)
    fin  = file(fname)
    fout = file(fname + ".out.py", "w")
    r1 = re.compile("^( *)[^ ]+")
    cnt_rest=cnt_empty=0
    tab_new = " " * to_tabs
    for lnr, line in enumerate(fin):
        m = r1.match(line)
        spaces = len(m.groups()[0])
        tabs = spaces // from_tabs
        rest = spaces % from_tabs
        if rest!=0:
            cnt_rest+=1
        content = line.lstrip()
        if content:
            fout.write(tab_new*tabs + " "*rest + content)
        else:
            cnt_empty+=1
            fout.write(line)
    cnt_match = (lnr+1-cnt_empty-cnt_rest)
    print "processed %s, from %d to %d spaces. Output in %s.\nLines %d, empty %d, not matching indent %d, matching indent %d (%.2f %%)." % (
           fname, from_tabs, to_tabs, fout.name, lnr+1, cnt_empty, cnt_rest, cnt_match, cnt_match/(lnr+1.0)*100.0)

if __name__=="__main__":
    if len(sys.argv)!=4:
        import os
        print """Usage: %s tabs_from tabs_to fname""" % os.path.basename(sys.argv[0])
        sys.exit(1)
    main(*sys.argv[1:])
