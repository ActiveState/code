## Python2 keyword-only argument emulation as a decorator. Python3 compatible.Originally published: 2016-04-10 00:52:25 
Last updated: 2016-04-15 13:25:20 
Author: István Pásztor 
 
Provides a very simple decorator (~40 lines of code) that can turn some or all of your default arguments into keyword-only arguments. You select one of your default arguments by name and the decorator turn this argument along with all default arguments on its right side into keyword only arguments. Check the docstring of the decorator or visit the github/pypi page for detailed documentation:\n\n- https://github.com/pasztorpisti/kwonly-args\n- https://pypi.python.org/pypi/kwonly-args\n\n`$ pip install kwonly-args`\n