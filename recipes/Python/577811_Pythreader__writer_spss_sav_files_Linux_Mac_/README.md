## Python reader + writer for spss sav files (Linux, Mac & Windows)  
Originally published: 2011-07-28 21:16:26  
Last updated: 2013-02-20 22:07:27  
Author: Albert-Jan Roskam  
  
**Python Program to READ & WRITE Spss system files (.sav) (Linux,Mac or Windows)**

* *Check https://pypi.python.org/pypi/savReaderWriter/ for the latest version (including the libraries!)*
* Requires libspssdio.so.1 (LINUX) or libspssdio.dylib (MAC) or spssio32.dll (WINDOWS) plus associated libaries, which can be freely downloaded from:
https://www.ibm.com/developerworks/mydeveloperworks/wikis/home/wiki/We70df3195ec8_4f95_9773_42e448fa9029/page/Downloads%20for%20IBM%C2%AE%20SPSS%C2%AE%20Statistics?lang=en
* It is recommended to download the v21 I/O files (required for writing zlib (.zsav) compressed files)
* December 2012 (complete rewrite):
- Added support for slicing, indexing, array slicing + other special methods
- Added support for writing spss date fields
- Added support for almost all meta data (missing values, sets, roles, etc.)
- Added support for 64 bit Windows (tested with Win7) and other OSs
  (z/Linux, Solaris, HP Linux, IBM AIX (untested though)
- Added support for reading and writing zlib compressed (.zsav) files
- Removed pesky segfault error when freeing memory
- Removed errors related to encoding
- Changed some Reader defaults (verbose=False, returnHeader=False)
- Renamed SavDataDictionaryReader into SavHeaderReader


**LINUX:**

*Installation (tested on Linux Ubuntu 10):*
* additional packages/files needed are: intel-icc8-libs_8.0-1_i386.deb,libicu32_3.2-3_i386.deb, libstdc++5_3.3.6-20_i386.deb, libirc.so.
* Run the following commands in your terminal: sudo apt-get install intel-icc8-libs; sudo apt-get install libicu32; sudo apt-get install libstdc++5.
* Then convert libirc.a (static) to libirc.so (dynamic), save in same location as libspssdio.so.1:
ar vx intel-icc8-libs_8.0-1_i386.deb; tar -xzvf data.tar.gz ./usr/lib/libirc.a; ar -x libirc.a.

*Calling the program:*
* In the TERMINAL  type: export LD_LIBRARY_PATH=/path/of/additional/sofiles; python /some/path/wrapperToProgram.py. You may also add ld_library_path to .bashrc
* The wrapper starts with "from SavReaderWriter import *", followed by e.g. stuff from the if __name__ == '__main__' section

**MAC OS:**
* you must put all the dylib files that come with the IBM 
SPSS_Statistics_InputOutput_Modules_* package in the macos
directory somewhere that OS X can find them
* one simple way to accomplish this is to copy them to /usr/lib

**WINDOWS:**
* You can also find this dll in the installation directory of SPSS (although SPSS is _not_ needed!)
* The .dll should be saved in the same location as this program.

**USAGE:**
See docstrings + __main__ section