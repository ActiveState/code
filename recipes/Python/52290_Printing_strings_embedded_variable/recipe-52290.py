"""VarString.py

Define the VarString class that encapsulates a string with embedded
variables.  For example:

from VarString import VarString

fromAddr = '"Samuel Clemens" <sam@marktwain.com>'
msg = VarString('''From: $fromAddr
To: $toAddr
Subject: A short message

Dear $toName,

Just a quick message to let you know that reports of my death
are greatly exaggerated.

Regards,
Samuel Clemens.
''')
# infoSource() returns a list of 2-tuples.
for toAddr, toName in infoSource():
    sendMsg(str(msg))

"""

import types, re, sys

class VarString:
    """A string with embedded variables signified by $a $b etc."""
    def __init__(self, string, immediate=None):
        if type(string) != types.StringType:
            raise TypeError
        self.__immediate = immediate
        if immediate:
            self.__str = self.__process(string)
        else:
            self.__str = string

    def __str__(self):
        if self.__immediate:
            return self.__str
        else:
            return self.__process(self.__str)

    def __process(self, str):
        r = re.compile("\$([A-Za-z_][A-Za-z0-9_]*)")
        self.__caller_globals, self.__caller_locals = _caller_symbols()
        newstr = r.sub(self.__embsub, str)
        return newstr
        

    def __embsub(self, match):
        name = match.group(1)
        if self.__caller_locals.has_key(name):
            return str(self.__caller_locals[name])
        elif self.__caller_globals.has_key(name):
            return str(self.__caller_globals[name])
        else:
            raise NameError, "There is no variable named '%s'" % (name)

def _caller_symbols():
    """Global and local symbols from three calling frames back

    Thanks to Itamar Shtull-Trauring for showing how this is done."""
    try:
        raise StandardError
    except StandardError:
        fr = sys.exc_info()[2].tb_frame
        # We go back three calling frames: to __process() to
        # __init__() or __str__() to its caller.
        return (fr.f_back.f_back.f_back.f_globals,
                fr.f_back.f_back.f_back.f_locals)
