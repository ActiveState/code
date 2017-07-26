## Drawing inheritance diagrams with "Dot"  
Originally published: 2003-08-03 07:54:55  
Last updated: 2003-08-03 07:54:55  
Author: Michele Simionato  
  
Dot is a very nice graph description language developed\nat MIT and available for free at http://www.graphviz.org/ .\nCombined with Python, it makes an ideal tool to automatically\ngenerate diagrams.\nI will describe here a short recipe which produces beautiful\ninheritance diagrams for Python classes (and metaclasses too).\nIn particular the recipe allows to display the MRO (Method\nResolution Order) for complicate inheritance hierarchies.