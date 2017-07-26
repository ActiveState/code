## wx twisted support using threads  
Originally published: 2004-07-06 13:21:53  
Last updated: 2004-07-06 13:21:53  
Author: Matthew Sherborne  
  
This script allows using twisted with wxPython at the same time without them stepping on each others toes.
I'm so sorry for the messyness of it. I haven't found the time to tidy it up.
The thing is it works, we use it in our kiosk administration program.
<ad>http://www.sherborneinternational.com</ad>.

wxPython has its own main loop, twisted has its own main loop.
wxreactor allows them to work together unless you want to use modal
dialogs (and in my case didn't work on two linux machines with wx2.4).
wxsupport is about the same, but didn't work on windows (with wx2.5) for me.

This solution is taken from itamar's suggestion in the twisted mailing list.
Let each run in its own thread.