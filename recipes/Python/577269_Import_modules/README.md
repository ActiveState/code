## Import modules in lambda functions  
Originally published: 2010-06-16 20:13:14  
Last updated: 2010-06-16 20:13:15  
Author: roopeshv   
  
I am not sure how many know that we can import modules inside lambda functions. So I am writing this to make the feature standout.

Instead of having the following function, which joins the paths

    import os
    relative_to_current = lambda *x: os.path.join(os.path.dirname(__file__), *x)

    # current directory is suppose /home/user/ (on linux) OR C:\Users (on Windows)
    >>> relative_to_current('Desktop')
    '/home/user/Desktop' # on linux
    'C:\\Users\\Desktop'

Here is same thing without having to import os in the module.