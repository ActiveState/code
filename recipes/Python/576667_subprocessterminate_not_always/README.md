## subprocess.terminate() not always implemented 
Originally published: 2009-02-25 10:40:04 
Last updated: 2009-02-25 10:45:01 
Author: Gui R 
 
The new subprocess module brings clarity and simplicity over the popenXX() functions and os.spawnXX() functions, but some implementations don't have the subprocess.terminate() method, which is crucial for killing a spawned process. This workaround works on both POSIX and Windows.