#!/usr/bin/env python
#
# Copyright (c) 2009 Andrew Grigorev <andrew@ei-grad.ru>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#


import sys
from ctypes import *
from threading import Thread


nfct = CDLL('libnetfilter_conntrack.so')
libc = CDLL('libc.so.6')


NFCT_CALLBACK = CFUNCTYPE(c_int, c_int, c_void_p, c_void_p)

# conntrack
CONNTRACK = 1
EXPECT = 2

# netlink groups
NF_NETLINK_CONNTRACK_NEW         = 0x00000001
NF_NETLINK_CONNTRACK_UPDATE      = 0x00000002
NF_NETLINK_CONNTRACK_DESTROY     = 0x00000004
NF_NETLINK_CONNTRACK_EXP_NEW     = 0x00000008
NF_NETLINK_CONNTRACK_EXP_UPDATE  = 0x00000010
NF_NETLINK_CONNTRACK_EXP_DESTROY = 0x00000020

NFCT_ALL_CT_GROUPS = (NF_NETLINK_CONNTRACK_NEW | NF_NETLINK_CONNTRACK_UPDATE \
    | NF_NETLINK_CONNTRACK_DESTROY)

# nfct_*printf output format
NFCT_O_PLAIN = 0
NFCT_O_DEFAULT = NFCT_O_PLAIN
NFCT_O_XML = 1
NFCT_O_MAX = 2

# output flags
NFCT_OF_SHOW_LAYER3_BIT = 0
NFCT_OF_SHOW_LAYER3 = (1 << NFCT_OF_SHOW_LAYER3_BIT)
NFCT_OF_TIME_BIT = 1
NFCT_OF_TIME = (1 << NFCT_OF_TIME_BIT)
NFCT_OF_ID_BIT = 2
NFCT_OF_ID = (1 << NFCT_OF_ID_BIT)

# callback return code
NFCT_CB_FAILURE = -1   # failure
NFCT_CB_STOP = 0       # stop the query
NFCT_CB_CONTINUE = 1   # keep iterating through data
NFCT_CB_STOLEN = 2     # like continue, but ct is not freed

# message type
NFCT_T_UNKNOWN = 0
NFCT_T_NEW_BIT = 0
NFCT_T_NEW = (1 << NFCT_T_NEW_BIT)
NFCT_T_UPDATE_BIT = 1
NFCT_T_UPDATE = (1 << NFCT_T_UPDATE_BIT)
NFCT_T_DESTROY_BIT = 2
NFCT_T_DESTROY = (1 << NFCT_T_DESTROY_BIT)
NFCT_T_ALL = NFCT_T_NEW | NFCT_T_UPDATE | NFCT_T_DESTROY
NFCT_T_ERROR_BIT = 31
NFCT_T_ERROR = (1 << NFCT_T_ERROR_BIT)


class ConntrackEventListener(Thread):
    def __init__(self, callback, msg_types=NFCT_T_NEW|NFCT_T_DESTROY):
        Thread.__init__(self)
        
        self.h = nfct.nfct_open(CONNTRACK, NFCT_ALL_CT_GROUPS)

        if self.h == 0:
            libc.perror("nfct_open")
            raise Exception("nfct_open failed!")
        
        buf = create_string_buffer(1024)
        self._stop = False

        def event_callback_closure(type, ct, data):
            nfct.nfct_snprintf(buf, 1024, ct, type, NFCT_O_XML, NFCT_OF_TIME)
            callback(buf.value)
            if self._stop:
                return NFCT_CB_STOP
            return NFCT_CB_CONTINUE

        self.cb = NFCT_CALLBACK(event_callback_closure)

        nfct.nfct_callback_register(self.h, msg_types, self.cb, 0)

    def run(self):
        ret = nfct.nfct_catch(self.h)
        
        nfct.nfct_callback_unregister(self.h)
        nfct.nfct_close(self.h)
        
        if ret == -1:
            libc.perror("nfct_catch")
            raise Exception("nfct_catch failed!")

    def stop(self):
        self._stop = True

__all__ = ["ConntrackEventListener", "NFCT_T_NEW", "NFCT_T_UPDATE", "NFCT_T_DESTROY", "NFCT_T_ERROR"]

if __name__ == "__main__":
    l = ConntrackEventListener(lambda x: sys.stdout.write("%s\n" % x))
    l.start()
    try:
        input()
    except:
        pass
    sys.stdout.write("Terminating (waiting for last event...)\n")
    l.stop()
    l.join()
