## Dictionary Who's Keys Act Like Attributes As WellOriginally published: 2011-02-28 04:05:43 
Last updated: 2011-05-26 20:15:16 
Author: Sunjay Varma 
 
Think of this as a JavaScript object. In JavaScript, the objects can be referenced by indexing (e.g. d[name]) or by directly using the dot (.) operator (e.g. d.name).\n\nThis is the same concept. \n\n**Note to Python 2.4 Users:** You will need to change the "except KeyError as e:" line to "except KeyError, (e):".