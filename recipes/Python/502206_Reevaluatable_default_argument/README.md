## Re-evaluatable default argument expressions

Originally published: 2007-02-03 19:13:34
Last updated: 2007-02-04 05:04:41
Author: George Sakkis

This recipe extends the standard python semantics with respect to default function arguments by allowing "deferred" expressions, expressions that are evaluated on every call instead of just once at function definition time.