## Get user info on Windows, for current user

Originally published: 2001-07-22 08:29:04
Last updated: 2001-07-22 08:29:04
Author: Wolfgang Strobl

Calling win32net.NetUserGetInfo(None, win32api.GetUserName(), 1) works for users logged in to the local machine, only, but fails for domain users. The snippet below demonstrates how to query the domain controller if there is one.