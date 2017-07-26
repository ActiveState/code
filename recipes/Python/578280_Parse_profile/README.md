## Parse profile  
Originally published: 2012-10-06 17:09:58  
Last updated: 2012-10-12 23:40:55  
Author: Jason Friedman  
  
    export VAR1=foo
    export VAR2=bar
    export VAR3=$VAR1$VAR2
    export VAR4=${VAR1}$VAR2
      export VAR5=${VAR1}indent
    export VAR6="text${VAR1} " # With embedded spaces and a comment
    export VAR7='${VAR4}' # Leave text within tics as-is

will be read as:

    {'VAR1': 'foo',
     'VAR2': 'bar',
     'VAR3': 'foobar',
     'VAR4': 'foobar',
     'VAR5': 'fooindent',
     'VAR6': 'textfoo ',
     'VAR7': '${VAR4}'}
