## command line query  
Originally published: 2010-03-09 17:45:14  
Last updated: 2010-03-09 18:37:52  
Author: Trent Mick  
  
Ask the user a question using raw_input() and looking something
like this (`style=="compact"`):

    QUESTION [DEFAULT]: _
    ...validation...

or this (`style=="verbose"`):

    QUESTION
    Hit <Enter> to use the default, DEFAULT.
    > _
    ...validate...

It supports some basic validation/normalization of the given answer.

See also: Recipe 577058 (query yes/no), Recipe 577097 (query yes/no/quit), Recipe 577096 (query custom answers)