## Multiple unique class instances - a tentative design pattern 
Originally published: 2013-02-23 14:11:43 
Last updated: 2013-02-23 14:11:44 
Author: Moritz Beber 
 
Coming from Bioinformatics and having to deal with multiple objects with unique properties, like genes, proteins, and many more, I felt the need for a class that would always yield a unique instance based on a chosen identifier. This is because I always wanted the same instances whose attributes were filled with information and track them in various storage classes, like dictionaries, lists, etc. The code for the class lives [over on github](https://github.com/Midnighter/unique-base). Recently, I've added a lot of parallel-processing code so I adapted the pickling behaviour for this class to also yield existing instances. What follows is an example of how to use it and some discussion questions.