"""

    A Longest common subsequence (LCS) problem solver.

    This problem is a good example of dynamic programming, and also has its
    significance in biological applications.

    For more information about LCS, please see:

    http://en.wikipedia.org/wiki/Longest_common_subsequence_problem
    
    Copyright 2009 Shao-Chuan Wang <shaochuan.wang@gmail.com>

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.

"""
__author__ = "Shao-Chuan Wang"
__email__ = "shaochuan.wang@gmail.com"
__version__ = "1.0"
__URL__ = "http://shao-chuan.appspot.com"

import functools

def cached(func):
  cache = {}
  def template(*args): #: template is wrapper; func is wrapped
    key = (func, )+args
    try:
      ret = cache[key]
    except KeyError:
      ret = func(*args)
      cache[key] = ret
    else:
      pass
    return ret

  functools.update_wrapper(template, func)
  return template

@cached
def LCSLength(str1, str2):
  if len(str1)==0 or len(str2)==0:
    return 0
  if str1[-1] == str2[-1]:
    return LCSLength(str1[:-1], str2[:-1])+1
  else:
    return max(LCSLength(str1, str2[:-1]), LCSLength(str1[:-1], str2))

@cached
def LCS(str1, str2):
  if len(str1)==0 or len(str2)==0:
    return ''
  if str1[-1] == str2[-1]:
    return ''.join([LCS(str1[:-1], str2[:-1]), str1[-1]])
  else:
    candidate1 = LCS(str1[:-1], str2)
    candidate2 = LCS(str1, str2[:-1])
    if len(candidate1) >= len(candidate2):
      return candidate1
    else:
      return candidate2

if __name__=='__main__':
  # a simple example
  lcs = LCS('abcbdab', 'bdcaba')
  assert len(lcs) == LCSLength('abcbdab', 'bdcaba')
  print 'Length of Longest common subsequence: %d' %(len(lcs),)
  print 'Longest common subsequence: %s' % (lcs,)

  # a complex example:
  strA = '''abcdefgabcdefgaabcdefgabcdefgabcdesdqfgabcdefgabcdefgabcdefgabcdefgabcdefgabcdefgabcdefg'''
  strB = '''gdebcdehhglkjlkabvhgdebcdehhgdebcdehhgdebcdeoshhgdebcdehhgdebcdehhgdebcdehhgdebcdehh'''
  lcs = LCS(strA, strB)
  assert len(lcs) == LCSLength(strA, strB)
  print 'Length of Longest common subsequence: %d' %(len(lcs),)
  print 'Longest common subsequence: '
  print lcs
  
