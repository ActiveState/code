## Accurate "Look before you leap" for safer (but still full) polymorphism

Originally published: 2001-03-21 06:11:12
Last updated: 2001-03-21 06:11:12
Author: Alex Martelli

Python functions are naturally polymorphic on their arguments, and checking argument types loses polymorphism -- but we may still get early checks and some extra safety without any real cost.