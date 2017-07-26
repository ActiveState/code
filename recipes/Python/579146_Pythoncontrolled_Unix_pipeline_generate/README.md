## Python-controlled Unix pipeline to generate PDF  
Originally published: 2016-01-07 18:02:51  
Last updated: 2016-01-07 18:02:52  
Author: Vasudev Ram  
  
This recipe shows how to create a Unix pipeline that generates PDF output, under the control of a Python program. It is tested on Linux. It uses nl, a standard Linux command that adds line numbers to its input, and selpg, a custom Linux command-line utility, that selects only specified pages from its input, together in a pipeline (nl | selpg). The Python program sets up and starts that pipeline running, and then reads input from it and generates PDF output.
