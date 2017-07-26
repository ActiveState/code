## 8 Queens Problem

Originally published: 2007-03-26 20:36:33
Last updated: 2007-03-26 20:36:33
Author: Calder Coalson

This relatively simple program solves by iteration the classic 8 queens chess problem.  For those unfamiliar, the challenge is to find the number of ways it's possible arrange 8 queens on a chess board so that none can capture any other in one move.  There's some wierd mathmatical proof of this, but this simple Python program demonstrates recursive iteration through many, (8^8), possible possibilities in the most efficient manor possible.  The code itself was written for clarity and speed by someone relatively new to Python, so it should be pretty easy to understand.