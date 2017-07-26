## A Python decorator that re-executes the function on conditionOriginally published: 2012-07-24 08:23:41 
Last updated: 2012-07-24 09:51:48 
Author: Chaobin Tang (唐超斌) 
 
Sometimes we want a function to be able to be retried automatically, such as a function that does networking trying to write/read data through a pre-established connection. Instead of writing try/except everywhere, a decorator would save much code and provide a single copy of code to do all the work.