## safer serialization of simple python types  
Originally published: 2005-05-29 21:13:08  
Last updated: 2005-06-02 08:35:45  
Author: S W  
  
Unpickling from an untrusted source, such as a network connection, can allow maliciously formed pickles to run arbitrary code.

This recipe presents a simple solution for serializing and unserializing simple Python types. Only simple Python types can be serialized, which makes the use of this algorithm safer than using the pickle module.

NB: I've changes this recipe drastically. It used to use a rather slow string slicing technique, which was a very bad example of how to use strings in Python! The cStringIO provided a faster, simpler replacement. This recipe now serializes faster than the Pickle module (not cPickle).

NB: A Python 2.4 version of this recipe is available here:
http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/415791