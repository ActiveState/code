## Distributed request/reply middleware architecture.Originally published: 2001-10-14 01:39:22 
Last updated: 2001-10-14 01:39:22 
Author: Graham Dumpleton 
 
Simple example of setting up a distributed message oriented request/reply architecture. Shows creation of a central exchange service which all participating processes connect to. Services assign themselves a name and export the methods which are remotely accessible. Client services are then able to make calls against the exported methods.