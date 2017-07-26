## Version-specific import  
Originally published: 2008-09-17 10:55:36  
Last updated: 2008-09-17 11:25:48  
Author: Michael   
  
Let's say you're at a company and you're deploying a package called "tools" on all production boxes.  Normally, code on these boxes could "import tools" to use this package.

However, over time the API to tools will evolve as you release new versions that add functionality and fix bugs.  If there's lots of company code that "imports tools", then you're stuck with backward compatibility forever.

This recipe presents a method for letting client code specify on one line which version of "tools" they wish to use -- and then import from the tools package as normal.  Behind the scenes, the recipe is making sure that the client works with the version of the package that they requested.  If the client ever wants to change versions, it's a one-line change at the top of their code.