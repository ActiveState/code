## Import modules in lambda functionsOriginally published: 2010-06-16 20:13:14 
Last updated: 2010-06-16 20:13:15 
Author: roopeshv  
 
I am not sure how many know that we can import modules inside lambda functions. So I am writing this to make the feature standout.\n\nInstead of having the following function, which joins the paths\n\n    import os\n    relative_to_current = lambda *x: os.path.join(os.path.dirname(__file__), *x)\n\n    # current directory is suppose /home/user/ (on linux) OR C:\\Users (on Windows)\n    >>> relative_to_current('Desktop')\n    '/home/user/Desktop' # on linux\n    'C:\\\\Users\\\\Desktop'\n\nHere is same thing without having to import os in the module.