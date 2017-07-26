# noinput.py
#
# A single line only to add after any imports to remove the contentious
# "input()" function from Python 1.4.0 to 2.7.2.
#
# This forces "input()" to become "raw_input()" and overrides the internel
# function for the current Python session. This means that if you really
# want the "input()" function you are forced to use the
# "eval(raw_input('Some Prompt:- '))" equivalent, or, to be cheeky, the
# Python 3.x.x "eval(input('Some Prompt:- '))" equivalent... ;o)
#
# I suspect this is not particularly well known so it is issued as
# Public Domain.
#
# Tested on classic AMIGAs, E-UAE, Debian 6.0.0, PCLinuxOS 2009,
# Windows and WinUAE using Python 1.4.0, 2.0.1, 2.4.2, 2.5.2, 2.6.1
# 2.6.6 and 2.7.2...

input=raw_input

# That is all there is to it! Just fifteen ASCII characters in one line...
# Enjoy finding simple solutions to often very difficult problems... ;o)
# Bazza, G0LCU...
