## Right method names suggestion

Originally published: 2005-04-06 14:03:04
Last updated: 2006-02-06 21:45:56
Author: bearophile -

My first recipe here, it uses __getattr__ to modify the error messages given when a wrong class method is called. It shows the first five ranked most similar method names, followed by the first line of their docstrings (this is useful to see their parameters, if you use this convention in your sources), and then it raises an AttributeError. Useful from the interactive shell too.