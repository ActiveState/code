## Tkinter Desktop Notifications or Popups  
Originally published: 2017-04-01 19:16:16  
Last updated: 2017-04-01 19:27:59  
Author: Miguel Martínez López  
  
This trick requires *pytweening*:

https://pypi.python.org/pypi/PyTweening

Install writing:

     pip install pytweening

It shows a notification on one corner of the screen,and gradually the notification disappears using an easing function. By default, it uses a linear easing function.

The class *Notification_Manager* has the method *create_notification*, but it also has some convenient methods to create easily some kind of notifications: success, alert, info, warning.