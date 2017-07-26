## List/Generator Monad Combinators

Originally published: 2005-08-18 07:16:04
Last updated: 2005-08-19 08:34:06
Author: Dominic Fox

The List monad in Haskell has many uses, including parsing and nondeterministic algorithms. This code implements the Monad combinators "bind", "return" and "fail", and the MonadPlus combinators "plus" and "zero". It works with all iterables, and returns a generator rather than a list in order to preserve a lazy semantics.