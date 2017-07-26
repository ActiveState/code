## Drawing inheritance diagrams with "Dot"  
Originally published: 2003-08-03 07:54:55  
Last updated: 2003-08-03 07:54:55  
Author: Michele Simionato  
  
Dot is a very nice graph description language developed
at MIT and available for free at http://www.graphviz.org/ .
Combined with Python, it makes an ideal tool to automatically
generate diagrams.
I will describe here a short recipe which produces beautiful
inheritance diagrams for Python classes (and metaclasses too).
In particular the recipe allows to display the MRO (Method
Resolution Order) for complicate inheritance hierarchies.