## Simplify Assignment to Member Variables 
Originally published: 2002-10-19 04:09:35 
Last updated: 2002-10-19 04:09:35 
Author: Jimmy Retzlaff 
 
Writing code like this can be very repetitive:\n\nclass c:\n&nbsp; &nbsp; &nbsp; &nbsp;def __init__(self, memberVariableNumberOne, memberVariableNumberTwo):\n&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;self. memberVariableNumberOne = memberVariableNumberOne\n&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;self. memberVariableNumberTwo = memberVariableNumberTwo\n\nThe above can be changed to:\n\nclass c:\n&nbsp; &nbsp; &nbsp; &nbsp;def __init__(self, memberVariableNumberOne, memberVariableNumberTwo):\n&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;AssignMemberVariablesFromParameters()