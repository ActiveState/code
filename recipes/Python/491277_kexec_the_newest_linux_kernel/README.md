###kexec the newest linux kernel

Originally published: 2006-04-20 14:38:21
Last updated: 2007-03-20 05:32:17
Author: Scott Tsai

Kexec is a mechanism to use linux itself to load a new kernel without going\nthrough the BIOS thus minimizing down time.\nThis script kexecs the newest kernel on the system managed by rpm (assumes a Redhat like system).