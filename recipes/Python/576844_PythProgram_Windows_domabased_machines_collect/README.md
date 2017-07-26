## Python Program for Windows domain based machines to collect usefull information (admins- software installed)  
Originally published: 2009-07-16 06:49:00  
Last updated: 2009-07-16 06:49:00  
Author: mgarrana Garrana  
  
this is a python program Python Program for Windows domain based machines to collect usefull information , this can be very customizable to the type of information you'd want to collect.
you can force it to run on all machines using group policy, and each machine would create a file in a specific folder ( for simplicity here , no need to go to a database at this level) with the machine name , and containing such information
for example , this program collects local administrators on the machine( can be very usefull in security assesments or securing the corporate ) , a list of all the software installed on the machine 
also other general information like machine name ,current logged on user , system time at script run time and domain that this machine belongs to

i've ran it in practice and i was really amazed by the result , that i couldn't find with any other tool
once you get the idea ... you can go wild with your dreams and do anything you like
i've also written a backend parser which parses the results and prints out a report with the required results
this program needs python for win32 installed
the program uses windows registery , win32 api
if you will run this software by group policy , you don't have to install python and python for windows extenstions onto each clinet machine
there is a tool called py2exe which magically , complies the code into and exe and DLL files , that you can run the exe by group policy as a startup script
please excuse the qualtiy of the code , as i am not a programmer , i am sys admin