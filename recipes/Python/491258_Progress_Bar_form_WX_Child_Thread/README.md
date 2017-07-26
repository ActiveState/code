## Progress Bar form WX in Child Thread of Main Python Code.  
Originally published: 2006-04-14 02:27:47  
Last updated: 2006-04-14 09:30:59  
Author: cheeng shu chin  
  
I come across some cases, where I need to hook a progress bar from WX to my current running python project/script to indicate the current process progress.
Some how if you use MainLoop() in child thread will cause the WX session hang and EVT handle will failed.
After some study, found that WXAPP class instance and MainLoop have to same namespace.
I manage to redesign it and make it work now.
Just mail/vote me, if you feel this is useful for your project.
E-Mail : cheengshuchin@gmail.com