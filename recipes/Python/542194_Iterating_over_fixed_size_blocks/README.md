## Iterating over fixed size blocks  
Originally published: 2008-01-12 17:58:28  
Last updated: 2008-01-12 17:58:28  
Author: George Sakkis  
  
This recipe shows a generator that breaks an iterable into chunks of fixed size. It addresses the general use case of having to (or wanting to) constrain the number of items to be processed at a time, for example because of resource limitations. It can very easily wrap blocks of code that work on iterables: just replace
<pre>process(all_items)</pre>with
<pre>for some_items in iterblock(all_items, 100):
    process(some_items)</pre>