## Recursively walk Python objects

Originally published: 2011-12-13 09:32:08
Last updated: 2011-12-23 22:10:38
Author: Yaniv Aknin

A small function that walks over pretty much any Python object and yields the objects contained within (if any) along with the path to reach them. I wrote it and am using it to validate a deserialized data-structure, but you can probably use it for many things.