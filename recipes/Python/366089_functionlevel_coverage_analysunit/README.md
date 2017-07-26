## function-level coverage analysis for unit tests  
Originally published: 2005-02-06 21:47:04  
Last updated: 2005-02-17 18:50:03  
Author: scott moody  
  
Use this recipe to provide simple function/method coverage analysis within your unit test suites using the following steps within a unit test file:

import myModule
<b>import coverage</b>

<b>coverage.ignore=[</b>myModule.myClass1,myModule.function7,...<b>]</b>
<b>coverage.watch(</b>myModule<b>)</b>

class TestMyModule:
&nbsp;&nbsp;&nbsp;&nbsp;def test_one(self):
 &nbsp;&nbsp;&nbsp;&nbsp;.
 &nbsp;&nbsp;&nbsp;&nbsp;.
&nbsp;&nbsp;&nbsp;&nbsp;.
&nbsp;&nbsp;&nbsp;&nbsp;def test_coverage(self):
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;assert <b>coverage.uncovered()</b>==[]

     where:
  '<i>myModule</i>' is the module being tested.
  '<i>coverage</i>' is the name given to the module containing this recipe.
  '<i>coverage.ignore</i>' is an optional list of functions/methods/classes to be excluded from the coverage analysis.
  '<i>coverage.watch(module_or_class)</i>' is called for each module and/or class to include in the coverage analysis.
  '<i>coverage.uncovered()</i>' returns a list of functions/methods that were not called over the course of the unit test and that are not covered by the ignore list.