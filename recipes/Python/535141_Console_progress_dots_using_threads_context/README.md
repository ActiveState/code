## Console progress dots using threads and a context manager  
Originally published: 2007-11-28 05:29:11  
Last updated: 2007-11-28 05:29:11  
Author: Paul Moore  
  
When executing a long running task, it is often useful to provide some feedback to the user. In a console program, this often consists of text such as "Running...." where a dot is printed (say) each second.

Adding a progress indicator like this to existing code can be tricky, but with threads and a context manager, it's easy.