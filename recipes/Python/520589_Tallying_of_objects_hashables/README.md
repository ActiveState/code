## Tallying of objects (hashables)Originally published: 2007-05-21 03:01:31 
Last updated: 2007-05-21 03:01:31 
Author: klausman-aspn  
 
This class can be used to tally objects, for example when analyzing log files. It has two separate ways of calculating the "score board", one quicker for Python >=2.4 and one that works with older versions (though I doubt it works with anything <2.0).\n\nAs the class uses a dictionary, only hashables can be counted. Other than that, you can mix and match them however you want.