## Win32 named mutex class for system-wide mutex

Originally published: 2011-07-15 21:12:40
Last updated: 2011-07-15 21:12:40
Author: Ben Hoyt

NamedMutex is a class for using Windows (Win32) named mutexes for system-wide locks. For example, we use these to lock system-wide log files that multiple processes can write to.