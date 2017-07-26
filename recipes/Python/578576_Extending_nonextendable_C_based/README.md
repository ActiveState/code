## Extending non-extendable C++ based Python classes

Originally published: 2013-06-20 17:22:11
Last updated: 2013-07-18 10:02:59
Author: Ahmet Emre Aladağ

graph_tool library is based on boost C++ library and provides Vertex class binding for Python. If we wanted to extend this Vertex class and add some attributes and methods, it wouldn't let us do that due to private constructor in C++ code (RuntimeError: This class cannot be instantiated from Python). We can overcome this obstacle using Proxy pattern.\n\nIn the __getattr__ method, if the attribute(or function name) is not in the Subclass MyVertex, then it looks for attributes of Vertex object that is defined inside MyVertex.