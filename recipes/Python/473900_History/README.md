## History and completion for the python shell  
Originally published: 2006-02-17 18:43:19  
Last updated: 2006-02-17 18:43:19  
Author: Vinko Vrsalovic  
  
This script creates a history file to share between your interactive python sessions, controlling its size in either lines or bytes. You have to put it in your PYTHONSTARTUP environment variable. As it uses readline, it only works under Unix systems. It also binds the tab key to complete words in the shell