## Parallelize your shell commands

Originally published: 2010-03-31 18:16:17
Last updated: 2010-04-02 00:14:38
Author: Kevin L. Sitze

This script is used to processes a batch job of commands in parallel.  The script dispatches new commands up to a user specified limit, each generated from a template provided on the command line using arguments taken from STDIN.  The basic combining semantics are similar to "xargs -1", though support for multiple arguments and parallel processing of commands are provided.