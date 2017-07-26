###List iterator with advance() and regress().

Originally published: 2002-08-02 08:31:54
Last updated: 2002-08-02 08:31:54
Author: Michael Chermside

The basic iterator for a list is a very "fast-but-dumb" design. It doesn't allow one to skip forward (except with "continue"), or backward (at all), nor does it behave well if the list is modified while it is being traversed. The following is NOT the be-all and end-all of improved iterators, but it gives a few ideas of how a better one might be created.