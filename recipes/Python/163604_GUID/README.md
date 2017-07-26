## GUID  
Originally published: 2002-11-21 16:08:37  
Last updated: 2006-01-05 19:53:25  
Author: Conan Albrecht  
  
A globally unique identifier that combines ip, time, and random bits.  Since the time is listed first, you can sort records by guid.  You can also extract the time and ip if needed.  GUIDs make wonderful database keys.  They require no access to the database (to get the max index number), they are extremely unique, and they sort automatically by time.