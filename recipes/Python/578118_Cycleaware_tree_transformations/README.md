## Cycle-aware tree transformationsOriginally published: 2012-05-02 16:55:13 
Last updated: 2012-06-20 08:09:13 
Author: Sander Evers 
 
A variation on Recipe 578117 that can deal with cycles. A cycle means that a tree has itself as a subtree somewhere. A fold over such a data structure has a chicken-and-egg-problem: it needs its own result in order to construct its own result. To solve this problem, we let `branch` construct a *part* of its result before going into recursion. After the recursion, `branch` gets a chance to complete its result using its children's results. Python's support for coroutines (using `yield`) provides a nice way to define such a two-stage `branch` function.