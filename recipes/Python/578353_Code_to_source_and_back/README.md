## Code to source and back

Originally published: 2012-12-01 06:19:38
Last updated: 2012-12-01 08:59:49
Author: Oren Tirosh

Converts a code object to a source code snippet and back: `c == recompile(*uncompile(c))`\n\nThis is useful, for example, if you want to apply an AST transformation to the code.\n\n