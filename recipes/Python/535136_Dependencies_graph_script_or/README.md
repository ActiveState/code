## Dependencies graph of a script or module 
Originally published: 2007-11-24 01:27:39 
Last updated: 2007-11-24 01:27:39 
Author: Oliver Schoenborn 
 
This is a recipe to generate a diagram of dependencies of a script. It uses Python's modulefinder to get the dependencies, the two scripts available from http://www.tarind.com/depgraph.html to generate a dot file, and graphviz to convert the dot file to PNG. It also filters out a lot of noise and facilitates configurability.