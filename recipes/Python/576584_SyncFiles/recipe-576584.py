#!/usr/bin/python

"""
This module makes it possible to ensure that data is not corrupted
between files whose version numbers are not important but must be
synchronized. It protects these files from crashes. It does, however,
require that critical files do not disappear between executions.
It can only account for cases where the computer does not do what it
is told, not cases where it does what it is not told.

Copyright (c) 2008 Collin Ross Mechlowitz Stocks

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os

class SyncFiles(object):
    def __init__(self,pathcons,*paths):
        self.pathcons=pathcons
        self.paths=list(paths)
        self.TEMP="-temp~"
        self.BACK="-back~"
        self.PACKETSIZE=1<<20
    def _testfiles(self):
        if os.path.exists(self.pathcons):
            #update had not even been called yet, so temps are bad
            #and currs are not bad
            return False,False
        tempsaregood=True
        currsarebad1=False
        currsarebad2=False
        if not os.path.exists(self.pathcons+self.TEMP):
            tempsaregood=False
            currsarebad1=True
        else:
            currsarebad2=True
        for path in self.paths:
            if not os.path.exists(path+self.TEMP):
                tempsaregood=False
                currsarebad1=True
            else:
                currsarebad2=True
        return tempsaregood,(currsarebad1 and currsarebad2)
    def _safeupdatefrom(self,ext):
        for path in self.paths:
            fread=open(path+ext,"rb")
            fwrite=open(path,"wb")
            data=fread.read(self.PACKETSIZE)
            while data:
                fwrite.write(data)
                data=fread.read(self.PACKETSIZE)
            fread.close()
            fwrite.close()
    def openread(self):
        ret=[]
        tempsaregood,currsarebad=self._testfiles()
        if tempsaregood:
            self._safeupdatefrom(self.TEMP)
            for path in self.paths:
                ret.append(open(path,"rb"))
        elif currsarebad:
            for path in self.paths:
                ret.append(open(path+self.BACK,"rb"))
        else:
            for path in self.paths:
                ret.append(open(path,"rb"))
        return ret
    def openwrite(self):
        ret=[]
        firsttime=True
        for path in self.paths:
            if os.path.exists(path):
                firsttime=False
        if not firsttime:
            tempsaregood,currsarebad=self._testfiles()
            if tempsaregood:
                self._safeupdatefrom(self.TEMP)
            elif currsarebad:
                self._safeupdatefrom(self.BACK)
        open(self.pathcons,"wb").close()
        for path in self.paths:
            ret.append(open(path+self.TEMP,"wb"))
        return ret
    def update(self):
        os.remove(self.pathcons)
        open(self.pathcons+self.TEMP,"wb").close()
        for path in self.paths:
            try:
                os.remove(path+self.BACK)
            except OSError:
                pass
        for path in self.paths:
            try:
                os.rename(path,path+self.BACK)
            except OSError:
                pass
        os.remove(self.pathcons+self.TEMP)
        for path in self.paths:
            os.rename(path+self.TEMP,path)
