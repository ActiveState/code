**********************************************************************
Begin Figure 1
**********************************************************************

// Written in Pseudo-Java/C++

interface InterfaceB {
  functionB1();
  functionB2();
}

class B implements InterfaceB {
  public:
    functionB1() {
      doStuff;
    }

    functionB2() {
      doMoreStuff;
    }
}

class A implements InterfaceB {
  private:
    B m_b;

  public:
    functionB1() {
      m_b->functionB1();
    }

    functionB2() {
      m_b->functionB2();
    }
}
**********************************************************************
End Figure 1
**********************************************************************


**********************************************************************
Begin Figure 2
**********************************************************************
#
# File: ProxyInterfaceOf.py
#

import types

def createProxyFunction(proxyObject):
    proxyObjectClassDict = proxyObject.__class__.__dict__

    # Create a function to forward requests to TargetObject.TargetFunction
    def ProxyFunction(self, *moreArgs, **evenMoreArgs):
        TargetObject, TargetFunction = proxyObjectClassDict["__functionMap"][ProxyFunction]
        return TargetFunction(TargetObject, *moreArgs, **evenMoreArgs)
    return ProxyFunction


def proxyInterfaceOf(ProxyObject, TargetObject):
    proxyObjectClassDict = ProxyObject.__class__.__dict__
    targetObjectClassDict = TargetObject.__class__.__dict__

    # Go through all the class attributes of the TargetObject
    for attribute in targetObjectClassDict:

        # If the attribute is a user defined function and not private.
        if ( (type(targetObjectClassDict[attribute]) is types.FunctionType )
             and (not attribute.startswith("__"))):

            # Create a function that forwards a function call to the TargetObject
            ProxyFunction = createProxyFunction(ProxyObject)

            # We need to be able to figure out the name of the function
            # the user is trying to call, so we create a mapping of
            # [ ProxyFunction : ( TargetObject, TargetFunction ) ]

            # Here we create the function map if it doesnt exist.
            if (not proxyObjectClassDict.has_key("__functionMap")):
                proxyObjectClassDict["__functionMap"] = dict()

            # Remember the TargetObject and the TargetFunction.
            TargetFunction = targetObjectClassDict[attribute]
            proxyObjectClassDict["__functionMap"][ProxyFunction] = (TargetObject, TargetFunction)

            # Create the same function in the ProxyObject that is in the TargetObject.
            proxyObjectClassDict[attribute] = ProxyFunction

**********************************************************************
End Figure 2
**********************************************************************


**********************************************************************
Begin Figure 3
**********************************************************************
from ProxyInterfaceOf import proxyInterfaceOf

#
# Simple Example of using proxyInterfaceOf()
#

class bar:
    def __init__(self):
        myFoo = foo(23)
        proxyInterfaceOf(self, myFoo) # I proxy all public foo functions


class foo:
    def __init__(self, appSpec):
        self.__appSpec = appSpec

    def func1(self):
        print "func1 :: internal data member self.__appSpec = " + str(self.__appSpec)

    def func2(self, arg1, arg2):
        print "func2 :: arg1 = " + str(arg1) + ", arg2 = " + str(arg2)

myBar = bar()
#print bar.__dict__
myBar.func1()
myBar.func2(34, "woo")

**********************************************************************
End Figure 3
**********************************************************************

Output from Figure 3:

func1 :: internal data member self.__appSpec = 23
func2 :: arg1 = 34, arg2 = woo
