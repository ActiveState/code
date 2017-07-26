## Managment command to deploy a Django project  
Originally published: 2011-06-21 22:07:35  
Last updated: 2011-06-21 22:10:31  
Author: Filippo Squillace  
  
This recipe shows a management command for django project that enables automatic synchronization between the local and remote project. Of course, the deploy exclude to overwrite the settings.py located in the remote server.\n\nThis is a clean way to deploy your own project without calling external commands, although this command needs rsync to work.