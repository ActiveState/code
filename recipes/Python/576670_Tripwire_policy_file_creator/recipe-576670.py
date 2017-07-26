#!/usr/bin/python
"""
gen_twpol.py    Copyright 2009 Bill Sharer

gen_twpol.py is a script that can be used to generate a tripwire policy source (twpol.txt) for your system.

This script may be distributed under the terms of the Gnu Public License GPLv2 or later.

For more information on the open source version of tripwire see http://sourceforge.net/projects/tripwire/

The tripwire source package usually ships with a an example twpol.txt file based on a RedHat Enterprise (RHEL)
distribution, typically an RHEL4 or RHEL5 version.  It doesn't do much good to have this get parked by your Gentoo
ebuild (nor other distro packager) as all sorts of stuff in /boot, /lib/modules and other places will be
out of sync, differently named or just plain missing.  In addition, your system may have extra stuff that isn't
present in the file but critical to the distro.

To use this script, park it in the tripwire config directory (probably /etc/tripwire).  Copy your existing twpol.txt
to twpol_header.txt and hack it up to remove the middle section of rules for the directories which will be scanned in
the crit_dir list.  You will want to keep the sections at the bottom for root's home dir and things like /home.  The
output from this script would then be appended to the header contents.

You will still want to tweak the root homedir rule section to take into account your prefs for window manager and the
settings for other dot files.  You should also do a quick sanity check of the output to fine tune the results before
generating a policy file with twadmin.  Since the list can be quite large, it may take 10 minutes or more for twadmin
to parse and create the encrypted policy.  A common problem is having a directory called out in a rule in the header
which is part of the crit_dirs and their subdirectories.  Tripwire doesn't like overlapping rules.
"""
import os
import re

#
#  These are all on a gentoo 64 bit distro but may be softlinked (/usr/lib to /usr/lib64).
#  On 64 bit RedHat or other 64 bit distros may see just /usr/lib instead of /usr/lib64
#  On 32 bit distros, will just have /usr/lib and no /usr/lib32 or /usr/lib64
#  You might consider tweaking to add /usr/local and other directories
#
crit_dirs = ("/boot", "/sbin", "bin", "/usr/sbin", "/usr/bin", "/lib", "/usr/lib", "/usr/lib32", "/usr/lib64", "/usr/libexec", "/etc")
#crit_dirs = ("/etc",)
#
#  Skip the following files and directories.  By default, tripwire watches its own files in a separate rule so we don't
#  want to duplicate.  If you decide to watch /var or /var/lib, you will probably want to include /var/lib/tripwire
#
#  The cron files will probably be covered in one of your header sections as "$(growing)"
#
#skip_dirs = ("/etc/tripwire", "/var/lib/tripwire")
skip_dirs = ("/etc/tripwire",)
skip_files = ("siggen", "tripwire", "twadmin", "twprint", "cron.daily", "cron.weekly", "cron.monthly")

#
#  Files ending with these extensions are include files, images, fonts and other junk that can usually be ignored
#
skip_types = (".keep", ".lock", ".zip", ".png", ".gif", ".jpg", ".h", ".hpp", ".c", ".cpp", ".txt", ".html", ".css", ".exsd", "Makefile", ".mak", ".cf", ".rules", ".tmpl", ".pmf", ".afm", ".idl", ".xsl")

#
#  Specials in a filename which will trip up the policy parser.  "$" gets used for anonymous java classes and appears with some frequency.
#  Thunderbird and Firefox like to use directories that are guid's stuck between braces.  May need to add more as we go along
#
skip_patterns = re.compile("[${}(),=]")

#
#  This gets tacked onto the end of each policy rule indicating what to watch for.  You may need to tweak this depending on your header.
#  
crit = "-> $(SEC_CRIT) ;"
#crit = "-> $(ReadOnly) ;"

#
#  which column do we space/tab over to before doing the crit string on the line
#
target_col = 100
blanks = "                                                                                                                                             "


#
#  Check a string to see if it's an item in a list
#
def found_in(string1, list1):
    for x in list1:
        if x == string1:
            return True
    return False


#
#  Check a string to see if it ends with an item on a list
#
def ends_with(string1, list1):
    for x in list1:
        if string1[-len(x):] == x:
            return True
    return False


#
#  output a single rule using whitespace to pad over to the action type
#
def do_rule(file1, string1):
    line = "  " + string1
    length = len(line)
    if length > target_col:
        line = line + blanks[:8] + crit + "\n"
    else:
        line = line + blanks[:(target_col-len(line)+1)] + crit + "\n"
    file1.write(line)
    
#
#  Check for twpol header in current directory
#
if os.path.isfile("./twpol_header.txt"):
    #
    #  Check for existing twpol.txt file and move out of the way
    #
    if os.path.isfile("./twpol.txt"):
        os.rename("./twpol.txt","./twpol.txt.old")
    #
    #  Copy the header to a new twpol.txt
    #
    headerfile = open("./twpol_header.txt","r")
    twpol = open("./twpol.txt","w")
    headerlist = headerfile.readlines()
    for header in headerlist:
        twpol.write(header)
    headerfile.close()
    
    #
    #  Iterate over each crit_dir
    #
    for crit_dir in crit_dirs:
        if os.path.islink(crit_dir):
            print "Ignoring softlinked directory ", crit_dir
        else:
            if os.path.isdir(crit_dir):
                #
                #  Dump the rule header lines
                #
                # rule_header = '\n\n(\n  rulename = "' + crit_dir + '",\n  severity = $(SIG_HI)\n)\n{\n'
                rule_header = '\n\n(\n  rulename = "' + crit_dir + '",\n)\n{\n'
                twpol.write(rule_header)
                do_rule(twpol,crit_dir+"/")
                #
                #  Walk the directory including subdirs and files
                #
                for path, subdirs, files in os.walk(crit_dir):
                    if found_in(path,skip_dirs):
                        print "*** Skipping subdirectory", path
                    else:
                        #
                        #  Do the directory or subdirectory itself
                        #
                        #do_rule(twpol,path+"/")
                        files.extend(subdirs)
                        files.sort()
                        for name in files:
                            filename = os.path.join(path, name)
                            if found_in(name,skip_files):
                                print "***Skipping file ", filename
                            else:
                                if ends_with(name,skip_types):
                                    print "***Skipping extension ", filename
                                else:
                                    if re.search(skip_patterns,filename) != None:
                                        print "***Skipping filename with bad chars ", filename
                                    else:
                                        #print filename
                                        do_rule(twpol,filename)
                twpol.write("}\n")
            else:
                print "*** %s is not a directory!" % crit_dir
    #
    #  
    twpol.close()
else:
    exit("No twpol_header.txt file present in this directory")
