## Composition of classes instead of multiple inheritance

Originally published: 2011-04-16 03:40:19
Last updated: 2011-04-16 03:40:19
Author: Ethan Furman

MI can be difficult and confusing, and if the base classes don't cooperate -- well, cooperative MI won't work.\n\nOne way around this is to use composition instead.  This class decorator will combine the source classes with the target class, ensuring that no duplications occur (raises a TypeError if there are any).