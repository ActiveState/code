#!/usr/bin/env python
####################################################################################
#                                                                                  #
# Copyright (c) 2013, Mike 'Fuzzy' Partin <fuzzy@fu-manchu.org>                    #
# All rights reserved.                                                             #
#                                                                                  #
# Redistribution and use in source and binary forms, with or without               #
# modification, are permitted provided that the following conditions are met:      #
#                                                                                  #
# 1. Redistributions of source code must retain the above copyright notice, this   #
#    list of conditions and the following disclaimer.                              #
# 2. Redistributions in binary form must reproduce the above copyright notice,     #
#    this list of conditions and the following disclaimer in the documentation     #
#    and/or other materials provided with the distribution.                        #
#                                                                                  #
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND  #
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED    #
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE           #
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR  #
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES   #
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;     #
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND      #
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT       #
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS    # 
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.                     #
#                                                                                  #
# The views and conclusions contained in the software and documentation are those  #
# of the authors and should not be interpreted as representing official policies,  #
# either expressed or implied, of the FreeBSD Project.                             #
#                                                                                  #
####################################################################################

############
## __NOTE__
############
#
# This is the processing engine code that provides the core of the DSL
#

import re, types

class InvalidArgument(Exception):
    """ Inavlid argument exception """
    pass
    
class Slurp:
    
    def __init__(self, ioObj=None):
        """ Instantiate a Slurp object
        
        Example:
        
        obj = Slurp(open('/etc/fstab', 'r'))
        # This will work for sockets and FIFO's as well
        
        """
        if ioObj != None:
            self.ioObj    = ioObj
            self.triggers = []
        else:
            raise InvalidArgument("A valid I/O object (file, socket, fifo) is required.\n")
            
    def register(self, patt=None, cback=None, final=True):
        """ Register a callback and associated pattern
        
        Slurp.register(patt=None, cback=None, final=True)
        
        Register a handler, using cback, when matching patt.
        If final is True, then Slurp will stop processing for that trigger, once it has
        matched it (this is on a per line basis).
        
        Example:
        
        obj = Slurp(open('/etc/fstab', 'r'))
        # Print only commented out lines
        obj.register('^#.*$', print)
        # *or*
        obj.register('^#.*$', print, False) # This will allow multiple callbacks to match        
        
        """
        # Check argument non-None..ness first and foremost
        if patt != None and cback != None:
            # Then check types
            if type(patt) != types.StringType or type(cback) != types.FunctionType:
                raise InvalidArgument
            else:
                # Check to see that our list of callbacks doesn't have one of these
                # instances already in it.
                for itm in self.triggers:
                    if itm[0] == patt:
                        return False
                # Ok, passed that, lets add it in
                self.triggers.append([patt, cback, final])
                return True
        else:
            raise InvalidArgument
            
    def process(self):
        """ Begin processing a given stream

        Example:

        obj = Slurp(open('/etc/fstab', 'r'))
        obj.register('^#.*$', print)
        obj.process()

        """
        # CAVEAT: The IO object *MUST* have a .readline() interface. This isn't much
        # of a showstopper as it's common, but a simple workaround would be to impliment
        # my own readline method (scanning for \n would work reasonably well) here inside
        # of Slurp to fall back on. I haven't hit a need for that yet, but this should
        # serve to remind me about it, if it ever comes up.
        buff = self.ioObj.readline()
        while buff:
            for pair in self.triggers:
                tmp_re = re.compile(pair[0])
                if tmp_re.match(buff):
                    # Call the callback with the line of text as the only argument
                    pair[1](buff.strip())
                    # Now lets see if we are a final measure
                    if pair[2] == False:
                        break
            # And refill the well.
            buff = self.ioObj.readline()

############
## __NOTE__
############
#
# This is the main execution logic
#

import sy
s
class Builder:
    def __init__(self, ioObj=None):
        if hasattr(ioObj, 'readline'):
            self.obj   = {}
            self.Slurp = Slurp(ioObj)
            handlers   = [
                # set the package name and version
                # Example: package 'ruby', '2.0.0-p0'
                ('^package\ +.*$',
                 self.setPackage),
                # set the uri or uri's for the package
                # Example: fetch_ur <uri>, <uri>, <uri>
                ('^fetch_uri\ +.*$', 
                 self.setUris),
                #
                ('^depends\ +.*$',
                 self.addDepends),
                #
                ('^configure_args\ +.*$',
                 self.configureArgs),
                #
                ('^make_args\ +.*$',
                 self.makeArgs),
            ]

    def setPackage(self):
        pass
    
    def setUris(self):
        pass
