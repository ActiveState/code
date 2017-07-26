# PROGRAM-NAME: readbin.py             BACKUP-REQUIRED: Yes
# AUTHOR: Tony Dycks                   REVISED BY: Tony Dycks
# DATE-WRITTEN: June 13, 2001          DATE-REVISED: June 20, 2001
# LANGUAGE: Active Python/Linux Python VERSION. NO.: 1.5.2 to 2.1
# PLATFORM: Win32/Linux (Text Console) VERSION. NO.: Any
#
# DESCRIPTION:
#   Display Hex And Character Contents Of File Entered On The Command Line.
#   Display 16 Characters Of Hex And Character Data Each Screen Line.  Pause
#   Display And Prompt For Continuation Every 20 Lines.  A Keyboard Entry
#   Of "X" <Enter> or "x" <Enter> Terminates The Program.  Any Other Key
#   Entry Continues The Display For Another 20 Lines.
#
# LIBRARY IMPORTS:
#   sys  Library Module For Screen I/O Functions And Exit To System
#   os   Library Module For Platform Clear Console Screen Function
#
# USAGE:
#   PYTHON readbin.py </Filepath/Filename.Ext> <Enter>   {Linux or Unix Implementations}
#   PYTHON readbin.py <D:\Filepath\Filename.Ext> <Enter> {Windows/Ms-DOS Implementations}
#
# USAGE EXAMPLE:
#   PYTHON readbin readbin.py <Enter>
#   {Displays This Source Program In ASCII and Hex Dump Format}
#
# REFERENCES: Adaptation of REXX Command Line Utility Program For Reading Binary
#   Files Using Python on a Win32 or Linux Terminal Console.
#
# TESTING SPECIFICS:
#   Program Has Been Tested On The Following Platforms And Versions Of Python: 
#
#   ----------------------------   ----------------------------------------------
#   Platform/Version               Python Version
#   ----------------------------   ----------------------------------------------
#   Red Hat Linux Version 6.1      Stichting Mathmatisch Centrum Amsterdam V1.5.2
#   Red Hat Linux Version 7.1      Stichting Mathmatisch Centrum Amsterdam V1.5.2
#   SuSE Linux Version 7.0         Stichting Mathmatisch Centrum Amsterdam V1.5.2
#   Microsoft Windows 98 SE        Active State Active Python Version 2.1
#   Microsoft Windows NT 4.0       Active State Active Python Version 2.1
#   Microsoft MS-DOS Version 7.0   Rational Systems, Inc. Version 1.97
#
# LIMITATIONS AND ASSUMPTIONS:
#   Execution From A Terminal Console OS Prompt Assumed.  Execution from within the
#   Python Interpreter Shell Requires Modification of argv Command Line
#   String Edits.  Program Has Been Tested On Terminal Console Windows For
#   The Following Platforms:  1) Red Hat Linux(tm) 6.1 Using Python Version 1.5.2,
#   2) SuSE Linux(tm) 7.0 Using Python Version 1.5.2, 3) Microsoft Windows 98 SE(tm)
#   Using Active State Active Python 2.1(tm).
#
#   Modification to the 'sys.platform' testing logic may be required for
#   implementations of Python, Windows, DOS or Linux that return a different
#   string value for the 'sys.platform' string property.
#
# PROGRAM MODIFICATION AND PLATFORM USAGE NOTES:
#   Use "import sys" and "print sys.platform" commands within Python Interpreter
#   To Determine Your  "sys.platform" value of Your Implementation Of Python If
#   Your OS Platform Is Something Other Than Red Hat Linux V6.1, SusE Linux V7.0,
#   or MS Windows 98 Second Edition under MS-DOS.  Platforms Other Than Linux,
#   Unix, Windows Or MS-DOS May Have A Value Other Than 'clear' or 'cls' For The
#   System Clear Terminal Screen Command.
#
# PROGRAM USE AND LICENSING:
#   Program is submitted under terms of the Python license and has been submitted
#   for consideration for inclusion in the upcoming O'Reilly Publication, 
#   "Python Cookbook".  Permission is granted for any editing or modification of 
#   the program for publication purposes.
#
# ==================================
# ==> Python Module Importations <==
# ==================================
import sys  # For OS Platform Determination
import os   # For Implementation of System Clear Terminal Screen Command,
            # Command Line Argument Processing and Exit To OS Prompt Function
# ================================
# ==> Constant Initializations <==
# ================================
dashln = '-' * 78
hexfmtlen = 6
# ==========================
# ==> Main Program Logic <==
# ==========================
#
# >>> Platform Testing <<<
#
# >>> Test Whether Program Is Being Run Under A Flavor Of Linux or Unix? <<<
# >>> Known Linux Implementations Tested Were Red Hat V6.1 and SuSE V7.0 <<<
if sys.platform == 'linux-i386' or sys.platform == 'linux2':
	SysCls = 'clear'
# >>> Test Whether Program Is Being Run Under Windows 32-bit Implementation <<<
elif sys.platform == 'win32' or sys.platform == 'dos' or sys.platform[0:5] == 'ms-dos':
	SysCls = 'cls'
# >>> Otherwise the Clear Screen Func is 'unknown' to prevent erroneous command execution <<<
else:
	SysCls = 'unknown'

def headings(argFile, argDashes, argSysCls): # Arguments are Filename, Line, Clr Scrn Fn Command
	if argSysCls != 'unknown':  # Is A Valid Clear Screen Command Known?
		os.system(argSysCls)      # Invoke System Clear Screen Display OS Command
	print 'File: ', argFile
	print argDashes
	return 0
	
def GetDisplayChar(argCharVal, argInChar): # Arguments are ASCII Char Value & Character Read
 	if charval < 32 or (charval > 127 and charval < 161):
		return '.'    # Use '.' to denote Non-displayable character
	else:
		return argInChar

if SysCls != 'unknown':  # Is A Valid Clear Screen Command Known?
	os.system(SysCls)      # Invoke System Clear Screen Display OS Command
# =================================
# ==> Print Program Info Banner <==
# =================================
print 'READBIN.PY -- Python Hex File Format Dump Command Line Utility For Binary Files'
print 'Version 1.0'
print 'By Tony Dycks'
print ' '
print 'Date Written: June 13, 2001'
print 'Date Last Revised: June 20, 2001'
print
print 'Submitted For Inclusion In The Python Cookbook'
print 'Open Source Contribution Under The GNU Public License'
print ' '
print ' '
print 'Running on System Platform:', sys.platform
print ' '
print 'Press <Enter> Key To Continue ... ',
response = sys.stdin.readline()
charln = ''
hexln = ''
offset = 0
offsetlen = 0
hexoffset = ''
charval = 0
charcnt = 0
# ################################################################################
# The following code will require mods if run from within the Python Interpreter
# ##############################################################################
# =========================================================================
# ==> No Command Line Argument Specified; Display Program Usage Message <==
# =========================================================================
if len(sys.argv) < 2:  
	print chr(7)  # ==> Beep Once <==
	print 'Incorrect Command Line Syntax ...'
	print ' '
	print 'Usage: Python readbin.py </Filepath/Filename.Ext> <Enter>'
	print ' '
	print sys.exit()
# =========================================================
# ==> Open File Specified On The Command Line For Input <==
# =========================================================
try:
	infile = open(sys.argv[1], 'r')   
	lncnt = headings(sys.argv[1], dashln, SysCls)  # Successful Return From Function Inits Line Counter
	while 1:  # ==> Read Until End Of File One Character At A Time <==
		inchar = infile.read(1)
		if not inchar:
			break
		charcnt = charcnt + 1
		charval = ord(inchar)
		hexval = hex(charval)
		hexstrlen = len(hexval)
		startpos = hexstrlen - 2
		if hexval[startpos] == 'x':
			startpos = startpos + 1
			hexval = '0'+hexval[startpos]
		else:
			hexval = hexval[startpos:hexstrlen]
		hexln = hexln+' '+hexval
		charln = charln + GetDisplayChar(charval, inchar)
		# ===================================================================
		# ==> 16 Characters Appended To String; Time To Print A Dump Line <==
		# ===================================================================
		if charcnt == 16:
			hexoffset = hex(offset)
			offsetlen = len(hexoffset)
			hexoffset = hexoffset[2:offsetlen]
			while len(hexoffset) < hexfmtlen:
				hexoffset = '0'+hexoffset
			print hexoffset+': '+hexln, ' | ', charln
			charln = ''
			hexln = ''
			charcnt = 0
			offset = offset + 16
			lncnt = lncnt + 1
			# ========================================================================
			# ==> A Screen-full of Info Displayed; Prompt for Continuation or Exit <==
			# ========================================================================
			if lncnt > 19:   
				print dashln
				print 'Press "X" <Enter> To Exit; <Enter> To Continue ... ',
				response = sys.stdin.readline()
				# =============================================================
				# ==> Take The First Character Slice of String, "response"; <==
				# ==> Test for Uppercase or Lowercase E<x>it response       <==
				# ======================================================--=====
				if response[0] == "X" or response[0] == 'x':
					break  # >>> Back to OS Console Prompt <<<
				else:
					# ====================================================
					# ==> Display Headings; Reset Screen Lines Counter <==
					# ====================================================
					lncnt = headings(sys.argv[1], dashln, SysCls)
except:
	print chr(7)  # >>> Beep Once <<<
	print 'Error Processing File:', sys.argv[1]
	print 'Terminating Program -- readbin.py'
	print ' '
	sys.exit()
# ============================
# ==> End Of Program Logic <==
# ============================
if len(charln) > 0:
	while len(charln) < 16:
		hexln = hexln + '   '
		charln = charln + ' '
		hexoffset = hex(offset)
		offsetlen = len(hexoffset)
		hexoffset = hexoffset[2:offsetlen]
	while len(hexoffset) < hexfmtlen:
		hexoffset = '0'+hexoffset
	print hexoffset+': '+hexln, ' | ', charln
# ===============================================
# ==> Successfully Processed The File Then    <==
# ==> Show Message and Exit Back To OS Prompt <==
# =============================================== 
print ' '
print '>>> End Of Program -- readbin.py <<<'
print ' '
sys.exit()
