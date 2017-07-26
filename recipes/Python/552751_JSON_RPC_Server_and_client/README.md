###JSON RPC Server and client

Originally published: 2008-04-01 09:50:49
Last updated: 2008-04-01 09:50:49
Author: david decotigny

This recipe shows how to create JSON RPC client and server objects. The aim is to mimic the standard python XML-RPC API both on the client and server sides, but using JSON marshalling. It depends on cjson (http://pypi.python.org/pypi/python-cjson) for the encoding/decoding of JSON data. This recipe tries to reuse the code of XML-RPC as much as possible.