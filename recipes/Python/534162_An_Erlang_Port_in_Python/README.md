## An Erlang Port in Python

Originally published: 2007-11-14 17:16:19
Last updated: 2010-02-18 06:47:09
Author: thanos vassilakis

Erlang has  two built-in interoperability mechanisms. One is distributed Erlang nodes and the other one is ports.\nPorts provide the basic Erlang mechanism for communication with the external world. They provide a byte-oriented interface to an external program. When a port has been created, Erlang can communicate with it by sending and receiving lists of bytes.  This recipe cooks an Erlang port in python. Making it easy for Erlang to instantiate and use python objects. Like most simple port implementations it uses an external python program and lets Erlang communicate via standard input and write to standard output. Theoretically, the external program could be written in any programming language. This recipe is pretty abstract and you will have to implement your own encode and decoding scheme.