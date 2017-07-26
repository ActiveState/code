###Tkinter Desktop Notifications or Popups

Originally published: 2017-04-01 19:16:16
Last updated: 2017-04-01 19:27:59
Author: Miguel Martínez López

This trick requires *pytweening*:\n\nhttps://pypi.python.org/pypi/PyTweening\n\nInstall writing:\n\n     pip install pytweening\n\nIt shows a notification on one corner of the screen,and gradually the notification disappears using an easing function. By default, it uses a linear easing function.\n\nThe class *Notification_Manager* has the method *create_notification*, but it also has some convenient methods to create easily some kind of notifications: success, alert, info, warning.