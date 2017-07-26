###Conjunction select using foreign keys

Originally published: 2011-06-11 02:43:21
Last updated: 2011-06-11 02:43:22
Author: Kaushik Ghose

Say we have a table (notes) containing rows we want to select. Each note has one or more keywords (stored in a table of the same name). We want to select notes that have a conjunction of keywords (AND). notes and keywords are linked through a foreign key table notes_keywords. The following SQL statement allows us to do this