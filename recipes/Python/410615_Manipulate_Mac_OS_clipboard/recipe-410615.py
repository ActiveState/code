#!/usr/bin/env python

"""Manipulate Mac OS clipboard ("scrap") from Python.

See also: pbcopy(1), pbpaste(1)"""

from sys import stdin, stdout
from optparse import OptionParser
from Carbon.Scrap import GetCurrentScrap, ClearCurrentScrap
import MacOS

def paste(flavorType='TEXT', verbose=False):
    try:
        scrap = GetCurrentScrap()
        return scrap.GetScrapFlavorData(flavorType)
    except MacOS.Error, e:
        if verbose or e[0] != -102:
            # -102 == noTypeErr
            raise
        return ""

def copy(text, flavorType='TEXT'):
    ClearCurrentScrap()
    scrap = GetCurrentScrap()
    scrap.PutScrapFlavor(flavorType, 0, text)

def list_flavors():
    scrap = GetCurrentScrap()
    return [(name, scrap.GetScrapFlavorSize(name))
            for name, flags in scrap.GetScrapFlavorInfoList()]

def main():
    parser = OptionParser()
    parser.set_defaults(flavor='TEXT', translate=True, copy=False,
                        list_=False, verbose=False)
    parser.add_option("-c", "--copy", dest="copy", action="store_true",
                      help="copy stdin to clipboard [default: paste clipboard"
                           " to stdout]")
    parser.add_option("-l", "--list", dest="list_", action="store_true",
                      help="list currently available flavors with data sizes")
    parser.add_option("-x", "--notrans", dest="translate",
                      action="store_false",
                      help="don't translate CR to LF on output")
    parser.add_option("-f", "--flavor", dest="flavor", action="store",
                      help="specify flavor [default: TEXT]")
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true",
                      help="complain if scrap flavor not found [default:"
                           " treat as empty]")
    
    options, args = parser.parse_args()
    if options.list_:
        for flavor in list_flavors():
            print "'%s' %9d" % flavor
    elif options.copy:
        copy(stdin.read(), options.flavor)
    else:
        text = paste(options.flavor, options.verbose)
        if options.translate:
            text = text.replace('\r', '\n')
        stdout.write(text)

__all__ = ['paste', 'copy', 'list_flavors', 'main']

if __name__ == "__main__":
    main()
