## Simplify Assignment to Member Variables  
Originally published: 2002-10-19 04:09:35  
Last updated: 2002-10-19 04:09:35  
Author: Jimmy Retzlaff  
  
Writing code like this can be very repetitive:

class c:
&nbsp; &nbsp; &nbsp; &nbsp;def __init__(self, memberVariableNumberOne, memberVariableNumberTwo):
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;self. memberVariableNumberOne = memberVariableNumberOne
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;self. memberVariableNumberTwo = memberVariableNumberTwo

The above can be changed to:

class c:
&nbsp; &nbsp; &nbsp; &nbsp;def __init__(self, memberVariableNumberOne, memberVariableNumberTwo):
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;AssignMemberVariablesFromParameters()