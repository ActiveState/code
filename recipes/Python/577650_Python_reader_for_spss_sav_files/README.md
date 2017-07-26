## Python reader for spss sav files  
Originally published: 2011-04-12 18:00:37  
Last updated: 2011-07-25 18:59:49  
Author: Albert-Jan Roskam  
  
**Python Program to read Spss system files (.sav)**

* ** version 2 (FASTER!) **
* Requires spssio32.dll, which can be freely downloaded from:
https://www.ibm.com/developerworks/mydeveloperworks/wikis/home/wiki/We70df3195ec8_4f95_9773_42e448fa9029/page/Downloads%20for%20IBM%C2%AE%20SPSS%C2%AE%20Statistics?lang=en
* You can also find this dll in the installation directory of SPSS (although SPSS is _not_ needed!)
* The .dll should be saved in the same location as this program.

* Parameters:
*savFileName*: the file name of the spss data file;
*returnHeader*: Boolean that indicates whether the first record 
  should be a list of variable names (default: True);
*recodeSysmisTo*: indicates to which value missing values should
  be recoded (default: "");
*selectVars*: indicates which variables in the file should be 
  selected.The variables should be specified as a list or a tuple 
  of valid variable names. If None is specified, all variables
  in the file are used (default: None);
*verbose*: Boolean that indicates whether information about the 
  spss data file (e.g., number of cases, variable names, file 
  size) should be printed on the screen (default: 
  True).            
*rawMode*: Boolean that indicates whether values should get 
  SPSS-style formatting,and whether date variables (if present) 
  should be converted to ISO-dates. If True, the program does not 
  format any values, which increases processing speed. (default: 
  = False)
*interfaceEncoding* Indicates the mode in which text communicated 
  to or from the I/O Module will be. Valid values are 'UTF-8' or 
  'CODEPAGE' (default = 'CODEPAGE')

* Typical use:
    savFileName = "d:/someFile.sav"
    with SavReader(savFileName) as sav:
        header = sav.next() 
        for line in sav:
            process(line)

* Note:
--*New version*: If you downloaded this previously, use the current version as it is **MUCH faster!!** 
--this code currently only works on Windows (32 bits). I might make it work on Linux Ubuntu 10 at some point.
--date fields in spss are represented as the number of seconds since the Gregorian calendar. The program converts these, wherever possible, to ISO-dates (yyyy-mm-dd).

Any feedback is welcome! I'm still learning!
