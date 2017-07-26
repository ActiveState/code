## Parse profile 
Originally published: 2012-10-06 17:09:58 
Last updated: 2012-10-12 23:40:55 
Author: Jason Friedman 
 
    export VAR1=foo\n    export VAR2=bar\n    export VAR3=$VAR1$VAR2\n    export VAR4=${VAR1}$VAR2\n      export VAR5=${VAR1}indent\n    export VAR6="text${VAR1} " # With embedded spaces and a comment\n    export VAR7='${VAR4}' # Leave text within tics as-is\n\nwill be read as:\n\n    {'VAR1': 'foo',\n     'VAR2': 'bar',\n     'VAR3': 'foobar',\n     'VAR4': 'foobar',\n     'VAR5': 'fooindent',\n     'VAR6': 'textfoo ',\n     'VAR7': '${VAR4}'}\n