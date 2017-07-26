# Title_Bar.py
# DEMO to show how to write some text into the Title Bar...
# Original code, (C)2013, B.Walker, G0LCU.
# Issued as Public Domain.
#
# Tested on OSX 10.7.5, Debian 6.0.x and PCLinuxOS 2009 using the default
# terminals running at least Python 2.5.2 to 3.3.2...
#
# A snapshot of the Title Bar here:-
#
# http://wisecracker.host22.com/public/Title_Bar.jpg
# To launch the DEMO enter:-
#
# >>> exec(open("/your/full/path/to/Title_Bar.py").read())<CR>
#
import time
#
print("Writing to the Title Bar...")
print("\x1B]0;THIS IS A TITLE BAR DEMO...\x07")
print("Wait for 5 seconds...")
time.sleep(5)
print("\x1B]0;\x07")
print("Title Bar returned to normal...")
#
# End of Title_Bar.py DEMO...
# Enjoy finding simple solutions to often very difficult problems...
