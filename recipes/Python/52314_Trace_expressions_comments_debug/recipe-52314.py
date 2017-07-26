import types, string, sys
from traceback import *

traceOutput = sys.stdout
watchOutput = sys.stdout
rawOutput = sys.stdout

""" Should print out something like:
File "trace.py", line 57, in __testTrace
  secretOfUniverse <int> = 42
"""
def watch ( variableName ):
    if __debug__:
        stack = extract_stack ( )[-2:][0]
        actualCall = stack[3]
        if ( actualCall is None ):
            actualCall = "watch ( [unknown] )"
        left = string.find ( actualCall, '(' )
        right = string.rfind ( actualCall, ')' )
        paramDict = { }
        paramDict["varName"]    = string.strip ( actualCall[left+1:right] )  # everything between '(' and ')'
        paramDict["varType"]    = str ( type ( variableName ) )[7:-2]
        paramDict["value"]      = repr ( variableName )
        paramDict["methodName"] = stack[2]
        paramDict["lineNumber"] = stack[1]
        paramDict["fileName"]   = stack[0]
        outStr = 'File "%(fileName)s", line %(lineNumber)d, in %(methodName)s\n  %(varName)s <%(varType)s> = %(value)s\n\n'
        watchOutput.write ( outStr % paramDict )


""" Should print out something like:
File "trace.py", line 64, in ?
  This line was executed!
"""
def trace ( text ):
    if __debug__:
        stack = extract_stack ( )[-2:][0]
        paramDict = { }
        paramDict["methodName"] = stack[2]
        paramDict["lineNumber"] = stack[1]
        paramDict["fileName"]   = stack[0]
        paramDict["text"]       = text
        outStr = 'File "%(fileName)s", line %(lineNumber)d, in %(methodName)s\n  %(text)s\n\n'
        traceOutput.write ( outStr % paramDict )


""" Should print out something like:
   Just some raw text
"""
def raw ( text ):
    if __debug__:
        rawOutput.write ( text )


def __testTrace ( ):
    secretOfUniverse = 42
    watch ( secretOfUniverse )	

if __name__ == "__main__":
    a = "something else"
    watch ( a )
    __testTrace ( )

    trace ( "This line was executed!" )
    raw ( "Just some raw text.." )
