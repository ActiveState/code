## Create a nested dictionary from os.walk  
Originally published: 2011-09-26 23:37:07  
Last updated: 2011-09-26 23:38:24  
Author: Andrew Clark  
  
Creates a nested dictionary that represents a folder structure.  Here is an example of what the resulting dictionary might look like:

    {
        "root": {
            "folder2": {
                "item2": None, 
                "item1": None
            }, 
            "folder1": {
                "subfolder1": {
                    "item2": None, 
                    "item1": None
                }, 
                "subfolder2": {
                    "item3": None
                }
            }
        }
    }