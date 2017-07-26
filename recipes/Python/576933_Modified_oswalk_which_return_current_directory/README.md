## Modified os.walk which return current directory depthOriginally published: 2009-10-18 15:10:50 
Last updated: 2009-11-06 16:16:42 
Author: Denis Barmenkov 
 
On some task I need to collect file names under specified directory with distance from it. Standard os.walk function do not return depth value.\n\nOne solution -- find function which will calculate relative distance from top directory to file.\n\nAnother [presented] solution -- modify os.walk so it returns depth level as fourth tuple's value.