## Retry Decorator in PythonOriginally published: 2017-01-11 10:09:17 
Last updated: 2017-01-11 10:10:30 
Author: Alfe  
 
This is a Python decorator which helps implementing an aspect oriented implementation of a *retrying* of certain steps which might fail sometimes.  A typical example for this would be communication processes with the outside world, e. g. HTTP requests, allocation of some resource, etc.  To use it, refactor the step in question into a (local) function and decorate this with the `retry` decorator.  See examples in the discussion sector below.