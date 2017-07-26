## Tripwire policy file creator  
Originally published: 2009-02-25 20:30:15  
Last updated: 2009-02-25 20:30:15  
Author: Bill Sharer  
  
gen_twpol.py is a script that can be used to generate a tripwire policy source (twpol.txt) for your system.

This script may be distributed under the terms of the Gnu Public License GPLv2 or later.

For more information on the open source version of tripwire see http://sourceforge.net/projects/tripwire/

The tripwire source package usually ships with a an example twpol.txt file based on a RedHat Enterprise (RHEL)
distribution, typically an RHEL4 or RHEL5 version.  It doesn't do much good to have this get parked by your Gentoo
ebuild (nor other distro packager) as all sorts of stuff in /boot, /lib/modules and other places will be
out of sync, differently named or just plain missing.  In addition, your system may have extra stuff that isn't
present in the file but critical to the distro.
