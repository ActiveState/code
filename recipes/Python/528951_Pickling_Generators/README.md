## Pickling Generators

Originally published: 2007-09-18 04:07:50
Last updated: 2007-10-09 07:37:31
Author: kay schluehr

This recipe is a followup of the Copying Generators recipe. It defines a GeneratorSnapshot object that stores all relevant data of a running generator but being serializable by pickle. During unpickling the generator is restored from the snapshot.