#!/usr/bin/env python
"""
    The MIT License
    
    Copyright 2009 Giuseppe Lo Brutto <giuseppelobrutto@gmail.com>

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.

"""


import sys
import wave

__author__  = "Giuseppe Lo Brutto"
__email__   = "giuseppelobrutto@gmail.com"
__version__ = "0.1"
__URL__     = ""



def printInfoPlayAudio(file=''):
		import ossaudiodev
		try:
			fd = wave.open(file, 'r')
			info = fd.getparams()
			print "numero canali: " + str(info[0])
			print "sample width: " + str(info[1])
			print "frame rate: " + str(info[2])
			print "numero frames " + str(info[3])
			print "tipo compressione: " + info[4]
			print "nome compressione: " + info[5]
			
			ad = ossaudiodev.open('/dev/audio','w')
			ad.setfmt(ossaudiodev.AFMT_U8)
			ad.channels(info[1])
			ad.speed(info[2])
			bytes = fd.readframes(1024)
			while bytes:
				ad.write(bytes)
				bytes = fd.readframes(1024)
			ad.flush()
			ad.sync()
		except IOError, e:
			print str(e)
		finally:
			fd.close()
			ad.close()
		
	
if __name__ == "__main__":
	assert(len(sys.argv)> 1)
	getInfo(sys.argv[1])
