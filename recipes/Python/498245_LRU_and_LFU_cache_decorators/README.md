###LRU and LFU cache decorators

Originally published: 2006-11-05 16:43:50
Last updated: 2010-08-01 01:19:23
Author: Raymond Hettinger

One-line decorator call adds caching to functions with hashable arguments and no keyword arguments.  When the maximum size is reached, the least recently used entry or least frequently used entry is discarded -- appropriate for long-running processes which cannot allow caches to grow without bound.  Includes built-in performance instrumentation.