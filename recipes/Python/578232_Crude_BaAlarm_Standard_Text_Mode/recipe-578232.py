# Baby_Alarm.py
#
# A very crude baby alarm or audio monitor using standard text mode Python.
#
# A simple program that will do a short record of sound from either the internal
# microphone or an external one and immediately replay it in a continuous loop.
# It should work on ANY version of Python for Linux from at least 2.0.1, but untested.
#
# This is similar to this Linux shell veraion:-
# guest:~$ cat /dev/dsp > /dev/dsp<CR>
# Except that the shell version generates a byte string 32768 bytes in size.
# Debian 6.0.0, /dev/dsp existing and Python 2.6.0, 2.7.2, 3.1.3...
# PCLinuxOS 2009, /dev/dsp existing and Python 2.5.2, 3.1.2...
# If /dev/dsp does not exist then install oss-compat from your distro's repository...
# It also assumes that the _MIXER_ is set up correctly...
#
# This is ALL there is to it...
#
# Have fun messing with the sound system in its basic mode... ;o)

print("\nA simple pseudo-baby alarm idea for Linux...\n")
print("$VER: Baby_Alarm.py_Version_0.00.10_(C)2012_B.Walker_G0LCU.\n")
audio=open("/dev/dsp", "rb")
sound=open("/dev/dsp", "wb")
def main():
	while 1:
		try: sound.write(audio.read(4000))
		except KeyboardInterrupt: break
main()
print("\b\b\b\bQuiting...")
sound.close()
audio.close()

# End of program.
# Enjoy finding simple solutions to often very difficult problems.
