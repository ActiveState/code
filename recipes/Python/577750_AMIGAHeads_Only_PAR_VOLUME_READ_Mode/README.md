## For AMIGA-Heads Only. PAR: As A VOLUME In READ Mode Only.  
Originally published: 2011-06-12 16:34:11  
Last updated: 2011-06-12 16:34:12  
Author: Barry Walker  
  
PAR: as a VOLUME in READ mode using Python 1.4 onwards on Classic AMIGAs...

Many years ago Irmen de Jong ported Python to the Classic AMIGA range of
computers, (many thanks Irmen for your time in doing so). The versions were
at least 1.4.x to 2.0.1 and now someone else has included version 2.4.6.

This gives we lowly users of the AMIGA at least a chance to see and use
Python in some guise or another. This code shows how to access the AMIGA
parallel port for 8 bit READ only. This is so that ADCs could be attached to
the port, read by Python code EASILY and utilised as a Data Logger/Transient
Recorder, as just one example.

There needs to be a single HW WIRE link only from the 23 way video port
to the 25 way parallel port for this to work. See the archive......

http://aminet.net/package/docs/hard/PAR_READ

......on how to set about this extremely simple task.

NO knowledge of the parallel port programming is needed at all to grab 8 bit
data from it using Python and other languages; (ARexx is used in the archive
above).

There is a flaw, NOTE:- NOT A BUG!, in the Python code but for this DEMO it
is ignored. ;o)

I'll let all you big guns work out what it is; you will need a good working
knowledge of the Classic AMIGA.

Enjoy finding simple solutions to often very difficult problems. ;o)

This code is Public Domain and you may do with it as you please.

Bazza...
