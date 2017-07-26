## Simple function base Genetic Algorithm 
Originally published: 2006-11-09 18:53:29 
Last updated: 2006-11-09 18:53:29 
Author: Ed Blake 
 
This is a solution to the first problem in this tutorial:\nhttp://www.ai-junkie.com/ga/intro/gat1.html\n\nI wrote it in about an hour, and tried to keep everything as clear and simple as possible.  Please excuse the sparse commenting.\n\nI deviated from the examples in the tutorial in several ways, the most important of which is the way the results are evaluated.  In the tutorial it is stated that the equations are solved from left to right, but for expedience I let Python's operator precedence determine the order of evaluation.  I'm not sure how close this example is to the example solution provided in the tutorial. I was to lazy to download unzip and decode the C source...