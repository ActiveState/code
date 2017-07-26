## cross-platform import hook for end-of-line conversion

Originally published: 2001-05-29 20:32:47
Last updated: 2001-05-29 20:32:47
Author: David Goodger

This code eliminates the need to convert line endings when moving .py modules between OSes.  Put in your sitecustomize.py, anywhere on sys.path, and you'll be able to import Python modules with any of Unix, Mac, or Windows line endings, on any OS.