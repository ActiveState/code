## Shell-like data processing, using Popen, pipes, and Thread  
Originally published: 2009-05-15 03:30:42  
Last updated: 2009-05-15 03:30:43  
Author: Massimo Santini  
  
This module is inspired by recipe 276960 and shows how external processes (istantiated with Popen) can be combined with a pipe-like syntax. Some support is added for having in the pipe also local functions (by caching their results in a ByteIO, or using operating system pipes). A similar approach, using generators, is presented in recipe 576756.