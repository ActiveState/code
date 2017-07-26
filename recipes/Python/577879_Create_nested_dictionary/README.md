###Create a nested dictionary from os.walk

Originally published: 2011-09-26 23:37:07
Last updated: 2011-09-26 23:38:24
Author: Andrew Clark

Creates a nested dictionary that represents a folder structure.  Here is an example of what the resulting dictionary might look like:\n\n    {\n        "root": {\n            "folder2": {\n                "item2": None, \n                "item1": None\n            }, \n            "folder1": {\n                "subfolder1": {\n                    "item2": None, \n                    "item1": None\n                }, \n                "subfolder2": {\n                    "item3": None\n                }\n            }\n        }\n    }