###Setting Win32 System Clock Using SNTP

Originally published: 2004-02-22 05:49:50
Last updated: 2004-02-22 05:49:50
Author: Robin Becker

Simon Foster's recipe "Simple (very) SNTP client"\n(see http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/117211)\ninspired me to get SNTP to do something useful when our office\nmoved to an ISP that didn't do client 37 time setting.\nThis recipe uses SNTP to get an estimate of the time offset\nand uses Thomas Heller's wonderful ctypes module to allow\ngetting/setting the win32 system time. I apologise in advance\nfor the rather awful int vs long bit twiddling in _L2U32 etc.