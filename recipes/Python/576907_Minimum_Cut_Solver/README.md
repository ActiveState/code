## Minimum Cut Solver  
Originally published: 2009-09-19 07:16:58  
Last updated: 2009-09-19 07:16:58  
Author: Shao-chuan Wang  
  
A Minimum Cut Solver
    
This python script is for solving the ACM problem Q2914: Minimum Cut.
http://acm.pku.edu.cn/JudgeOnline/problem?id=2914

Instead of using Ford-Fulkerson method, I use Stoer and Wagner's Min cut Algorithm.
http://www.cs.dartmouth.edu/~ac/Teach/CS105-Winter05/Handouts/stoerwagner-mincut.pdf

However I also include the max flow method (from wiki) for benchmark.
The code can be found at: http://en.wikipedia.org/wiki/Ford-Fulkerson_algorithm