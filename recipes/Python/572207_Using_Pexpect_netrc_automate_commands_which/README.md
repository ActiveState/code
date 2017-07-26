###Using Pexpect and netrc to automate commands which prompt for a password

Originally published: 2008-05-16 21:44:21
Last updated: 2008-05-17 04:54:46
Author: John Landahl

System administrators sometimes need to automate commands which prompt for a password (or any other single prompt) before they execute. This recipe demonstrates using Pexpect and the built-in netrc module to automate these commands easily and relatively securely.