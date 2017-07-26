# Linux Version...
# Fade_Linux.py
#
# $VER: Fade_Linux.py_Version_0.00.10_(C)2012_B.Walker_G0LCU.
#
# Written so that anyone can see and understand how it works! YES, it CAN be simplified considerably!!!
#
# This Linux version can easily be enhanced upon, e.g. cycling through colours...

import os
import sys
import time

# Ensure it works on just about all versions of Python...
if sys.version[0]=="3": raw_input=input

os.system("setterm -cursor off")
os.system("clear")
print("\nA DEMO to show fading and screen flashing...\n")
print("Press Ctrl-C to cycle through the test windows...\n")
print("$VER: Fade_Linux.py_Version_0.00.10_(C)2012_B.Walker_G0LCU.\n")
raw_input("Press ENTER to Continue:- ")

def main():
	os.system("clear")
	while 1:
		try:
			print("\033[12;23f\033[30mFading using four _shades_ of grey...\033[0m")
			time.sleep(0.1)
			print("\033[12;23f\033[90mFading using four _shades_ of grey...\033[0m")
			time.sleep(0.1)
			print("\033[12;23f\033[37mFading using four _shades_ of grey...\033[0m")
			time.sleep(0.1)
			print("\033[12;23f\033[0mFading using four _shades_ of grey...\033[0m")
			time.sleep(0.1)
			print("\033[12;23f\033[37mFading using four _shades_ of grey...\033[0m")
			time.sleep(0.1)
			print("\033[12;23f\033[90mFading using four _shades_ of grey...\033[0m")
			time.sleep(0.1)
		except KeyboardInterrupt: break
	print("\033[13;1f    \033[12;22f\033[30m                                       \033[0m")
	time.sleep(0.5)
	audio=open("/dev/dsp","wb+")
	# This next window CANNOT be done in Windows using CMD.EXE as the Terminal!
	while 1:
		try:
			print("\033[12;36f\033[0;91;40mDANGER!!!\033[0m")
			time.sleep(0.1)
			for n in range(0,680,1): audio.write(b"\x00\x00\x00\x3F\x3F\x3F")
			print("\033[12;36f\033[0;30;101mDANGER!!!\033[0m")
			time.sleep(0.1)
			for n in range(0,500,1): audio.write(b"\x00\x00\x00\x00\x3F\x3F\x3F\x3F")
		except KeyboardInterrupt: break
	os.system("clear")
	audio.close()
	time.sleep(0.5)
	audio=open("/dev/dsp","wb+")
	while 1:
		try:
			print("\033[0;91;40m")
			os.system("clear")
			print("\033[12;36f\033[0;91;40mDANGER!!!")
			time.sleep(0.1)
			for n in range(0,680,1): audio.write(b"\x00\x00\x00\x3F\x3F\x3F")
			print("\033[0;30;101m")
			os.system("clear")
			print("\033[12;36f\033[0;30;101mDANGER!!!")
			time.sleep(0.1)
			for n in range(0,500,1): audio.write(b"\x00\x00\x00\x00\x3F\x3F\x3F\x3F")
		except KeyboardInterrupt: break
	print("\033[0m")
	os.system("clear")
	audio.close()
	time.sleep(0.5)
main()

os.system("setterm -cursor on")

print("\n$VER: Fade_Linux.py_Version_0.00.10_(C)2012_B.Walker_G0LCU.\n")
print("Fading and flashing DEMO end...\n")

# End of Fade_Linux.py DEMO...
# Enjoy finding simple solutions to often very difficult problems... ;o)





# Windows Version...
# Fade_Windows.py
#
# $VER: Fade_Windows.py_Version_0.00.10_(C)2012_B.Walker_G0LCU.
#
# Written so that anyone can see and understand how it works! YES, it CAN be simplified considerably!!!
#
# This Windows version is limited compared to the Linux version but my be of use...

import os
import sys
import time
import winsound

# Ensure it works on just about all versions of Python...
if sys.version[0]=="3": raw_input=input

os.system("CLS")
print("\nA DEMO to show fading and screen flashing...\n")
print("Press Ctrl-C to cycle through the test windows...\n")
raw_input("Using CMD.EXE as the CLI this is limited; press ENTER to Continue:- ")

def main():
	while 1:
		try:
			os.system("CLS")
			os.system("COLOR 07")
			print("\n\n\n\n\n\n\n\n\n\n\n                                                            ")
			time.sleep(0.05)
			os.system("CLS")
			os.system("COLOR 08")
			print("\n\n\n\n\n\n\n\n\n\n\n                    This is a test string to check fading...")
			time.sleep(0.05)
			os.system("CLS")
			os.system("COLOR 07")
			print("\n\n\n\n\n\n\n\n\n\n\n                    This is a test string to check fading...")
			time.sleep(0.05)
			os.system("CLS")
			os.system("COLOR 0F")
			print("\n\n\n\n\n\n\n\n\n\n\n                    This is a test string to check fading...")
			time.sleep(0.05)
			os.system("CLS")
			os.system("COLOR 07")
			print("\n\n\n\n\n\n\n\n\n\n\n                    This is a test string to check fading...")
			time.sleep(0.05)
			os.system("CLS")
			os.system("COLOR 08")
			print("\n\n\n\n\n\n\n\n\n\n\n                    This is a test string to check fading...")
			time.sleep(0.05)
		except KeyboardInterrupt: break
	while 1:
		try:
			os.system("COLOR C0")
			os.system("CLS")
			print("\n\n\n\n\n\n\n\n\n\n\n                                    DANGER!!!")
			winsound.Beep(1333,600)
			os.system("COLOR 0C")
			os.system("CLS")
			print("\n\n\n\n\n\n\n\n\n\n\n                                    DANGER!!!")
			winsound.Beep(1000,600)
		except KeyboardInterrupt: break
	os.system("COLOR 0F")
	os.system("CLS")
main()

print("\n$VER: Fade_Windows.py_Version_0.00.10_(C)2012_B.Walker_G0LCU.\n")
print("Fading and flashing DEMO end...\n")

# End of Fade_Windows.py DEMO...
# Enjoy finding simple solutions to often very difficult problems... ;o)
