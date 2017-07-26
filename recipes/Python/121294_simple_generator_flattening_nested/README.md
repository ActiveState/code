## simple generator for flattening nested containers  
Originally published: 2002-04-17 17:53:37  
Last updated: 2002-04-17 17:53:37  
Author: H. Krekel  
  
this generator flattens nested containers such as

<code> l=( (1,23), [[[[42,(5,23)]]]])</code>

so that

<code> for i in flatten(l): print i</code>

gives you 1,23,42,5,23


