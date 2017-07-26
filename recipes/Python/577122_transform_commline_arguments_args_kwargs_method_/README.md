## transform command line arguments to args and kwargs for a method call  
Originally published: 2010-03-17 13:25:16  
Last updated: 2010-03-21 22:41:42  
Author: Trent Mick  
  
For many of my Python modules I find it convenient to provide a small `if __name__ == "__main__": ...` block to be able to call individual methods from the command line. This requires some kind of translation of command-line string arguments to `args` and `kwargs` for the method call. This recipe uses a few conventions to do that:

- the first argument is the method name
- positional args are positional (duh)
- "key=value" is a keyword argument
- an attempt is made to interpret arguments as JSON to allow specifying types other than string