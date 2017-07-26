## wx twisted support using threads  
Originally published: 2004-07-06 13:21:53  
Last updated: 2004-07-06 13:21:53  
Author: Matthew Sherborne  
  
This script allows using twisted with wxPython at the same time without them stepping on each others toes.\nI'm so sorry for the messyness of it. I haven't found the time to tidy it up.\nThe thing is it works, we use it in our kiosk administration program.\n<ad>http://www.sherborneinternational.com</ad>.\n\nwxPython has its own main loop, twisted has its own main loop.\nwxreactor allows them to work together unless you want to use modal\ndialogs (and in my case didn't work on two linux machines with wx2.4).\nwxsupport is about the same, but didn't work on windows (with wx2.5) for me.\n\nThis solution is taken from itamar's suggestion in the twisted mailing list.\nLet each run in its own thread.