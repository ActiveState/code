###Simple Linear Regression with Pure Python

Originally published: 2014-07-31 15:55:14
Last updated: 2014-07-31 15:55:15
Author: Chaobin Tang (唐超斌)

Linear regression is a very useful and simple to understand way for predicting values, given a set of training data. The outcome of the regression is a best fitting line function, which, by definition, is the line that minimizes the sum of the squared errors (When plotted on a 2 dimensional coordination system, the errors are the distance between the actual Y' and predicted Y' on the line.) In machine learning, this line equation Y' = b*x + A is solved using Gradient Descent to gradually approach to it. Also, there is a statistical approach that directly solves this line equation without using an iterative algorithm.\n\nThis recipe is a pure Python implementation of this statistical algorithm. It has no dependencies.\n\nIf you have pandas and numpy, you can test its result by uncommenting the assert lines.