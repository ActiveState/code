## Get the path of the currently executing  python script using import.  
Originally published: 2006-02-24 05:23:36  
Last updated: 2006-02-24 05:23:36  
Author: Jitender Cheema  
  
# 1. sys.arg has the script name
# 2. Although there can be many ways, e.g.  os.cwd() but, there is another
# trick to
# obtain the Complete URI or Location of the current script.
# You can argue,  os.getcwd()
# import can give you working directory of the current script
# Third party Java code calling your script.... ;)
#