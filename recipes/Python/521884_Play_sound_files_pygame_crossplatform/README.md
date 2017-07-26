## Play sound files with pygame in a cross-platform mannerOriginally published: 2007-06-04 15:19:54 
Last updated: 2007-06-21 14:16:58 
Author: Chris Arndt 
 
This simple script shows how to play back a sound file using the mixer module from the pygame library. If you have pygame installed, this will work on all major platforms. The mixer module supports WAV and OGG files with many different sample rates, bits per sample and channels. The script will play back all supported files given on the command line sequentially.