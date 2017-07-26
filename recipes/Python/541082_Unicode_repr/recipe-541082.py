def urepr(x):
    import re, unicodedata

    def toname(m):
        try:
            return r"\N{%s}" % unicodedata.name(unichr(int(m.group(1), 16)))
        except ValueError:
            return m.group(0)

    return re.sub(
        r"\\[xu]((?<=x)[0-9a-f]{2}|(?<=u)[0-9a-f]{4})",
        toname,
        repr(x)
    )

def displayhook(x):
    if x is not None:
        print urepr(x)

def install():
    import sys
    sys.displayhook = displayhook

def uninstall():
    import sys
    sys.displayhook = sys.__displayhook__
