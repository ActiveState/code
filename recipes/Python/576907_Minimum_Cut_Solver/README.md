## Minimum Cut Solver

Originally published: 2009-09-19 07:16:58
Last updated: 2009-09-19 07:16:58
Author: Shao-chuan Wang

A Minimum Cut Solver\n    \nThis python script is for solving the ACM problem Q2914: Minimum Cut.\nhttp://acm.pku.edu.cn/JudgeOnline/problem?id=2914\n\nInstead of using Ford-Fulkerson method, I use Stoer and Wagner's Min cut Algorithm.\nhttp://www.cs.dartmouth.edu/~ac/Teach/CS105-Winter05/Handouts/stoerwagner-mincut.pdf\n\nHowever I also include the max flow method (from wiki) for benchmark.\nThe code can be found at: http://en.wikipedia.org/wiki/Ford-Fulkerson_algorithm