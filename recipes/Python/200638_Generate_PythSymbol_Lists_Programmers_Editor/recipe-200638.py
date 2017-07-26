# GenEditorSymbolLists.py
"""Make lists of Python symbols for a programmer's editor syntax coloring file

Redirect this program's stdout to a text file.  Cut and paste some or all of
the lists to build a syntax coloring file for your prefered programmer's
editor.

Copyright 2003 by James M Jinkins - Released to the Public Domain

Jim -dot_ Jinkins -at_ ComPorts -dot_ com
"""

import keyword
import types
import re

COMMENT_CHR = ";"   # Set to the comment indicator of the editor program

specialNamePat = re.compile("^.*(__([a-zA-Z0-9]+(_[a-zA-Z0-9]+)*)__).*$")
methodPat = re.compile("^<(slot wrapper|method|built-in method) .+>$")
instancePat = re.compile("^<.+ (instance at) .+>$")

def sortRemoveDupes(lst):
    """Sort the list, and remove duplicate symbols.
    """
    if len(lst) == 0:
        return lst
    lst.sort()
    lst = [lst[0]] + [lst[i] for i in range(1, len(lst))
            if lst[i] != lst[i - 1]]
    return lst

def printList(lst, title):
    """Write a title line.  List the symbols in the list on separate lines.
    """
    print "\n\n\n%s %s %s %s symbols %s" % (COMMENT_CHR * 6, title,
            COMMENT_CHR * 3, len(lst), COMMENT_CHR * 6)
    if len(lst) == 0:
        print "%s%s%s" % (COMMENT_CHR * 8, "empty list", COMMENT_CHR * 8)
    else:
        for le in lst:
            print le

##############################################################################

if __name__ == "__main__":
    allKeywords = keyword.kwlist
    allKeywords.sort()

    allTypes = dir(types)
    allTypes.sort()

    allBuiltins = dir(__builtins__)
    allBuiltins.sort()
    # Split allBuiltins
    builtinExceptions = []
    builtinNames = []
    for attrName in allBuiltins:
        if attrName in ["license", "copyright", "credits", "help"]:
            builtinNames.append(attrName)
        else:
            try:
                obj = eval("%s()" % attrName)
                if isinstance(obj, Exception):
                    builtinExceptions.append(attrName)
                else:
                    builtinNonExceptions.append(attrName)
            except Exception, e:
                builtinNames.append(attrName)

    normalTypeMethods = []
    specialTypeMethods = []
    normalTypeAttrs = []
    specialTypeAttrs = []
    for typeName in dir(types):
        try:
            typeDir = dir(eval("types.%s" % typeName))
            for attrName in typeDir:
                try:
                    attr = eval("types.%s.%s" % (typeName, attrName))
                    attrRepr = repr(attr)
                    # print "        attrRepr = %s"% attrRepr
                    m = methodPat.match(attrRepr)
                    if m:
                        m = specialNamePat.match(attrName)
                        if m:
                            specialTypeMethods.append(attrName)
                        else:
                            normalTypeMethods.append(attrName)
                    else:
                        m = specialNamePat.match(attrName)
                        if m:
                            specialTypeAttrs.append(attrName)
                        else:
                            normalTypeAttrs.append(attrName)
                except Exception, e:
                    pass
                    # print "    attr=%s - %s" % (attr, e)
        except Exception, e:
            pass
            # print "    No dir -- %s" % e

    # These special methods are not in the list, because neither the object
    # class nor any standard types class needs them.
    specialTypeMethods.extend(["__complex__", "__del__"])

    normalObjectMethods = []
    specialObjectMethods = []
    normalObjectAttrs = []
    specialObjectAttrs = []
    obj = object()
    for attrName in dir(object):
        # print "attrName = %s" % attrName
        try:
            attr = eval("object.%s" % attrName)
            attrRepr = repr(attr)
            # print "    attrRepr = %s" % attrRepr
            m = methodPat.match(attrRepr)
            if m:
                m = specialNamePat.match(attrName)
                if m:
                    specialObjectMethods.append(attrName)
                else:
                    normalObjectMethods.append(attrName)
            else:
                m = specialNamePat.match(attrName)
                if m:
                    specialObjectAttrs.append(attrName)
                else:
                    normalObjectAttrs.append(attrName)
        except Exception, e:
            print "    object.%s  Exception %s" % (attrName, e)

    specialMethods = sortRemoveDupes(specialTypeMethods + specialObjectMethods)
    normalMethods = sortRemoveDupes(normalTypeMethods + normalObjectMethods)
    specialAttrs = sortRemoveDupes(specialTypeAttrs + specialObjectAttrs)
    normalAttrs = sortRemoveDupes(normalTypeAttrs + normalObjectAttrs)

    # Remove duplicate symbols
    for x in specialAttrs[:]:
        if x in specialMethods:
            specialAttrs.remove(x)
    for x in builtinNames[:]:
        if x in specialAttrs:
            builtinNames.remove(x)
    for x in allTypes[:]:
        if x in specialAttrs:
            allTypes.remove(x)

    printList(allKeywords, "Keywords")
    # printList(allBuiltins, "All builtin names")
    printList(builtinExceptions, "Builtin exception classes")
    printList(builtinNames,
            "Other Builtin names - Functions and other objects")
    printList(specialAttrs, "Special attributes of types and object")
    printList(specialMethods, "Special methods of types and object")
    printList(normalMethods, "Other methods of types and object")
    printList(normalAttrs, "Other attributes of types and object")
    printList(allTypes, "Type names")
