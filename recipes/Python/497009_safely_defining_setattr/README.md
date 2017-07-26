###"safely" defining __setattr__

Originally published: 2006-08-31 12:40:07
Last updated: 2006-09-01 08:06:29
Author: Ori Peleg

Overriding __setattr__ in classes requires care when setting attributes yourself. Here's an idea for safely setting attributes in __init__.\n\nUpdate: this idea doesn't work. See Mike Foord's recipe for one that does:\n\nhttp://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/389916