## command line query 
Originally published: 2010-03-09 17:45:14 
Last updated: 2010-03-09 18:37:52 
Author: Trent Mick 
 
Ask the user a question using raw_input() and looking something\nlike this (`style=="compact"`):\n\n    QUESTION [DEFAULT]: _\n    ...validation...\n\nor this (`style=="verbose"`):\n\n    QUESTION\n    Hit <Enter> to use the default, DEFAULT.\n    > _\n    ...validate...\n\nIt supports some basic validation/normalization of the given answer.\n\nSee also: Recipe 577058 (query yes/no), Recipe 577097 (query yes/no/quit), Recipe 577096 (query custom answers)