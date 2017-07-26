# DEMO code for recording a few seconds of sound and playing back the same
# from inside a terminal running standard Python 2.x in a Linux distro...
# (I think this is Python 3.x compatible too.)
#
# This assumes /dev/audio exists, if NOT, then install oss-compat
# from your distro`s repository.
#
# (Original idea copyright, (C)2010, B.Walker, G0LCU.)
# Now issued as Public Domain, (to LXF).
#
# You may do as you like with this idea but some acknowledgement
# would be appreciated.
#
# Save in the Python/Lib drawer(/folder/directory) as arp.py.
#
# Use "import arp<RETURN/ENTER>" without the quotes to test it.
#
# Once imported start talking loudly into a laptop`s internal microphone
# for about 6 seconds then wait for the recorded sound to be played back.
#
# Tested on PCLinuxOS 2009, Knoppix 5.1.1, (and Debian 6.0.0 <- WITH
# oss-compat installed).
#
# Ensure the sound system is not already in use.
#
# These two imports NOT needed for this quick demo.
# import sys
# import os

def main():
    global record
    record=""
    # Record from my Laptop`s, Notebook`s and Netbook`s mic.
    # Note sample rate unknown at the moment, (8KHz?).
    # Shout into the internal mic` for test purposes.
    audio=file('/dev/audio', 'rb')
    record=audio.read(65536)
    audio.close()
    # Playback from the sound card(s).
    audio=file('/dev/audio', 'wb')
    audio.write(record)
    audio.close()
main()

# End of record/playback DEMO.
# Enjoy finding simple solutions to often very difficult problems.
