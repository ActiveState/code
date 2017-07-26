## Clear Only Project Modules 
Originally published: 2014-12-17 19:03:14 
Last updated: 2014-12-17 19:03:15 
Author: Cornelius Jatniel Prinsloo 
 
Useful for python sessions that have a long startup time\nbecause of external dependancies\n[In my case that would be pygame and pymunk]\nI've got a slow computer so it takes a while to startup\nthis is the solution I came up with\n\nimport this before any other of your project imports\nexample:\n    import reloading # The modules in your project folder get cleared\nthen load the rest of your project modules\n\nmake sure that the reloading script is in your project folder, or else it won't work\n\nYou might be able to extend this by changing line