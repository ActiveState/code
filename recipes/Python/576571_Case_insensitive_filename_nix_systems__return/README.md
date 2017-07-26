## Case insensitive filename on *nix systems - return the correct case filename

Originally published: 2008-11-25 07:59:52
Last updated: 2008-11-25 16:27:13
Author: Campbell Barton

When dealing with windows paths on a *nix system sometimes youll need to resolve case insensitive paths. While using a fat filesystem or making everything lowercase would work.\nthis function means you can get python to take a case insensitive path and return the path with the correct case (if it exists).