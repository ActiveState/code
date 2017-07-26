## ilines -- universal newlines from any data source 
Originally published: 2004-06-23 11:33:52 
Last updated: 2004-06-23 11:33:52 
Author: Scott David Daniels 
 
ilines is a generator that takes an iterable and produces lines of text.  The input iterable should produce blocks of bytes (as type str) such as might be produced by reading a file in binary.  The output lines are formed by the same rule as the "universal newlines" file mode [f = file(name, 'U')] and are produced "on-line" -- when lines are discovered, they are produced.